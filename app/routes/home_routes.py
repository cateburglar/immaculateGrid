import logging
import os

import requests
from bs4 import BeautifulSoup
from flask import Blueprint, flash, jsonify, redirect, render_template, session, url_for
from flask_login import login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from app import db
from app.forms import LoginForm, SignupForm, TeamSummaryForm

from ..models import BattingStats, Fielding, PitchingStats, Teams, User

# Ensure the logging directory exists
log_dir = os.path.join("app", "logging")
os.makedirs(log_dir, exist_ok=True)

# Configure custom logger for home routes
log_file_path = os.path.join(log_dir, "home_logs.log")
logger = logging.getLogger("home_routes_logger")
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler(log_file_path)
formatter = logging.Formatter("%(asctime)s - %(message)s")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Configure custom logger for stats logs
stats_log_file_path = os.path.join(log_dir, "stats_logs.log")
stats_logger = logging.getLogger("stats_logger")
stats_logger.setLevel(logging.INFO)
stats_file_handler = logging.FileHandler(stats_log_file_path)
stats_file_handler.setFormatter(formatter)
stats_logger.addHandler(stats_file_handler)

home_routes = Blueprint("home_routes", __name__, template_folder="templates")


@home_routes.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(username=form.username.data).first()
        if not existing_user:
            # Hash the password
            hashed_password = generate_password_hash(
                form.password.data, method="scrypt"
            )

            # Create a new User instance
            new_user = User(
                nameFirst=form.nameFirst.data,
                nameLast=form.nameLast.data,
                username=form.username.data,
                password=hashed_password,
            )

            # Add the new user
            db.session.add(new_user)
            db.session.commit()

            # Log account creation
            logger.info(f"Account created: {new_user.username}")

            # Show a successs message and redirect to login
            flash("Account created successfully!", "success")
            login_user(new_user, remember=False)

            session["username"] = new_user.username

            # Log login
            logger.info(f"Successful login: {new_user.username}")

            flash(f"Welcome, {new_user.username}!", "success")
            return redirect(url_for("home_routes.home"))

        else:
            logger.info(f"Duplicate account creation attempt for {form.username.data}")
            flash("Username is already taken, please try again", "danger")
    return render_template("signup.html", title="Sign Up", form=form)


# /login
@home_routes.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Retrieve the user from the database
        user = User.query.filter_by(username=form.username.data).first()

        # Verify if the user exists and the password is correct
        if user and check_password_hash(user.password, form.password.data):
            # Log in the user
            login_user(user)
            logger.info(f"Successful login: {user.username}")
            session["username"] = user.username
            flash(f"Welcome, {user.nameFirst} {user.nameLast}!", "success")
            return redirect(url_for("home_routes.home"))

        logger.info(f"Failed login attempt: {form.username.data}")
        flash("Invalid username or password", "danger")

    return render_template("login.html", title="Sign In", form=form)


@home_routes.route("/logout")
def logout():
    # Log logout
    logger.info(f"Logout: {session["username"]}")

    # Logout user
    logout_user()

    # Clear session variables
    logger.info(f"Clearing {session["username"]} session variables")
    session.pop("returned_players", None)
    session.pop("returned_player_ids", None)
    session.pop("username", None)

    # Flash a message and redirect home
    flash("You have been logged out.", "info")
    return redirect(url_for("home_routes.login"))


@home_routes.route("/about", methods=["GET"])
def about():
    return render_template("about.html")


# /
@home_routes.route("/", methods=["GET", "POST"])
def home():
    form = TeamSummaryForm()

    if form.validate_on_submit():
        team_name = form.teamName.data
        year = form.yearID.data
        stats_logger.info(
            f"{session["username"]} requested team summary for {team_name}, {year}"
        )

        with db.session.no_autoflush:
            # Get team_ID matching the team_name
            result = (
                db.session.query(Teams.teamID)
                .filter(Teams.team_name == team_name, Teams.yearID == year)
                .first()
            )
            team_ID = result.teamID

            stats_logger.info(f"teamID returned for {team_name}, {year}: {team_ID}")
            if not team_ID:
                flash(f"No team found for {team_name} in {year}", "warning")
                stats_logger.error(
                    f"ERROR: Bad teamID returned for {team_name}, {year}"
                )
                return render_template("team_summary.html", form=form)

            # Get summary info
            batting_leaders = get_batting_leaders(team_ID, year)
            pitching_leaders = get_pitching_leaders(team_ID, year)
            depth_chart_data = getDepthChartData(team_ID, year)

            # Scrape the photo (If the year is too old there won't be one)
            photo = None
            if int(year) >= 1900:
                photo = get_baseball_reference_photo(team_ID, year)

            stats_logger.info(
                f"Depth chart info returned for {team_name}, {year}: {depth_chart_data}"
            )
            return render_template(
                "team_summary.html",
                form=form,
                batting_leaders=batting_leaders,
                pitching_leaders=pitching_leaders,
                teamName=team_name,
                teamID=team_ID,
                yearID=year,
                photo=photo,
                depth_chart_data=depth_chart_data,
            )

    return render_template("team_summary.html", form=form)


@home_routes.route("/get_years/<team_name>", methods=["GET"])
def get_years(team_name):
    years = TeamSummaryForm.get_years_for_team(team_name)
    return jsonify({"years": years})


def get_baseball_reference_photo(teamID, yearID):
    # Construct the URL for the player's page on Baseball-Reference
    url = f"https://www.baseball-reference.com/teams/{teamID}/{yearID}.shtml"

    # Send a GET request to fetch the page content
    response = requests.get(url)

    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, "html.parser")

        # Find the div element with the class "media-item"
        media_item_div = soup.find("div", {"class": "media-item"})

        if media_item_div:
            # Find the img element within the div
            img_tag = media_item_div.find("img")

            if img_tag and "src" in img_tag.attrs:
                # Return the image URL
                return img_tag["src"]
            else:
                stats_logger.warning(f"Image not available for {teamID}")
                return None
        else:
            stats_logger.warning(f"Media item div not found for {teamID}")
            return None
    else:
        stats_logger.error(f"Team not found for {teamID}")
        return None


def getDepthChartData(team_ID, year):
    # Query the database for the players on a team in a given year
    players = db.session.query(Fielding).filter_by(yearID=year, teamID=team_ID).all()
    if not players:
        flash("No players found for the selected team and year.", "info")
        return None

    stats_logger.info("Fetching depth chart")

    # Group players by position
    depth_chart_data = {}
    for player in players:
        position = player.position
        player_stats = None

        if position not in depth_chart_data:
            depth_chart_data[position] = []

        # get the stats for each player based on their position
        if position == "P":
            stats_logger.info("Getting pitcher stats")
            player_stats = (
                db.session.query(PitchingStats)
                .filter_by(yearID=year, teamID=team_ID, playerID=player.playerID)
                .first()
            )

        else:
            stats_logger.info("Getting batter stats")
            player_stats = (
                db.session.query(BattingStats)
                .filter_by(yearID=year, teamID=team_ID, playerID=player.playerID)
                .first()
            )

        # Skip players with bad data
        if player_stats == None or player_stats.playerID == None:
            continue

        # Add the player and their stat to the depth chart
        depth_chart_data[position].append(player_stats)

    return depth_chart_data


def preprocess_pitching_leaders(pitching_leaders):
    """Preprocess pitching leaders to handle None values and round numbers."""
    for leader in pitching_leaders:
        leader.p_ERA = round(leader.p_ERA or 0, 3)
        leader.p_FIP = round(leader.p_FIP or 0, 3)
        leader.p_K_percent = round(leader.p_K_percent or 0, 3)
        leader.p_BB_percent = round(leader.p_BB_percent or 0, 3)
        leader.p_HR_div9 = round(leader.p_HR_div9 or 0, 3)
        leader.p_BABIP = round(leader.p_BABIP or 0, 3)
        leader.p_LOB_percent = round(leader.p_LOB_percent or 0, 3)
        leader.age = round(leader.age or 0, 0)
        leader.p_G = round(leader.p_G or 0, 0)
        leader.p_GS = round(leader.p_GS or 0, 0)
        leader.p_IP = round(leader.p_IP or 0, 3)

    return pitching_leaders


# Utility function to fetch batting leaders
def get_batting_leaders(team_ID, year):
    batting_leaders_query = db.session.query(BattingStats).filter(
        BattingStats.yearID == year, BattingStats.teamID == team_ID
    )

    if not batting_leaders_query:
        flash(f"No batting leaders found for {team_ID} in {year}", "warning")
        stats_logger.error(f"ERROR: No batting leaders returned for{team_ID}, {year}")
        return None

    return batting_leaders_query.all()


# Utility function to fetch and preprocess pitching leaders
def get_pitching_leaders(team_ID, year):
    pitching_leaders_query = db.session.query(PitchingStats).filter(
        PitchingStats.yearID == year, PitchingStats.teamID == team_ID
    )
    if pitching_leaders_query:
        return preprocess_pitching_leaders(pitching_leaders_query.all())
    else:
        flash(f"No pitching leaders found for {team_ID} in {year}", "warning")
        stats_logger.error(f"ERROR: No pitching leaders returned for {team_ID}, {year}")
        return None
