import logging
import os

from flask import (
    Blueprint,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from flask_login import login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from app import db
from app.forms import DepthChartForm, LoginForm, SignupForm, TeamSummaryForm

from ..models import Batting, Fielding, Pitching, Teams, User

# Ensure the logging directory exists
log_dir = os.path.join("app", "logging")
os.makedirs(log_dir, exist_ok=True)

# Configure custom logger
log_file_path = os.path.join(log_dir, "home_logs.log")
logger = logging.getLogger("home_routes_logger")
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler(log_file_path)
formatter = logging.Formatter("%(asctime)s - %(message)s")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

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
            # Log in the user and manage 'remember me' option
            login_user(user, remember=form.remember_me.data)
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


# /
@home_routes.route("/", methods=["GET", "POST"])
def home():
    form = TeamSummaryForm()

    if form.validate_on_submit():
        # Get form data
        team_name = form.teamName.data
        year = form.yearID.data

        # Get team_ID matching the team_name
        result = (
            db.session.query(Teams.teamID)
            .filter(Teams.team_name == team_name, Teams.yearID)
            .first()
        )
        team_ID = result.teamID

        if not team_ID:
            flash(f"No team found for {team_name} in {year}", "warning")
            return render_template("team_summary.html", form=form)

        # Query the database for batting leaders---- TODO will be modded!!!!!!!!!!!!!!!!
        batting_leaders = (
            db.session.query(Batting)
            .filter(Batting.yearId == year, Batting.teamID == team_ID)
            .order_by(
                Batting.b_2B.desc(),
            )
            .all()
        )

        if not batting_leaders:
            flash(f"No batting leaders found for {team_name} in {year}", "warning")

        # Query the database for pitching leaders ----- TODO WILL BE MODDED !!!!!!!!!!!!!!!
        pitching_leaders = (
            db.session.query(
                Pitching.playerID, Pitching.p_W, Pitching.p_L, Pitching.p_SO
            )
            .filter(Pitching.yearID == year, Pitching.teamID == team_ID)
            .order_by(Pitching.p_W.desc(), Pitching.p_L.asc(), Pitching.p_SO.desc())
            .all()
        )

        if not pitching_leaders:
            flash(f"No pitching leaders found for {team_name} in {year}", "warning")

        return render_template(
            "team_summary.html",
            form=form,
            batting_leaders=batting_leaders,
            pitching_leaders=pitching_leaders,
            teamName=team_name,
            yearID=year,
        )

    return render_template("team_summary.html", form=form)


@home_routes.route("/get_years/<team_name>", methods=["GET"])
def get_years(team_name):
    years = TeamSummaryForm.get_years_for_team(team_name)
    return jsonify({"years": years})


def displayDepthChart(team_name, year, form):
    team_ID = team_name

    # Query the database for the player's batting stats for the given yearID and teamID
    # THIS WILL BE REPLACED BY BATTING STATS EVENTUALLY TODO
    players = db.session.query(Fielding).filter_by(yearID=year, teamID=team_ID).all()
    if not players:
        flash("No players found for the selected team and year.", "info")
        return render_template("depth_chart.html", form=form)
    # Group players by position
    depth_chart_data = {}
    for player in players:
        position = player.position
        if position not in depth_chart_data:
            depth_chart_data[position] = []
        # THIS WILL CONTAIN BATTING STATS TODO !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        depth_chart_data[position].append(player)

    return render_template(
        "depth_chart.html",
        form=form,
        yearID=year,
        teamName=team_name,
        depth_chart_data=depth_chart_data,
    )
