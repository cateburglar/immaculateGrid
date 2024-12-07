import logging
import os

from flask import Blueprint, jsonify, render_template, session
from sqlalchemy import desc, or_

from app import db
from app.forms import LeaguesForm

from ..models import Teams

# Ensure the logging directory exists
log_dir = os.path.join("app", "logging")
os.makedirs(log_dir, exist_ok=True)

# Configure custom logger
log_file_path = os.path.join(log_dir, "league_logs.log")
logger = logging.getLogger("league_routes_logger")
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler(log_file_path)
formatter = logging.Formatter("%(asctime)s - %(message)s")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

league_routes = Blueprint("league_routes", __name__, template_folder="templates")


@league_routes.route("/", methods=["GET", "POST"])
def get_league():
    form = LeaguesForm()

    if form.validate_on_submit():
        lgID = form.teamName.data
        year = form.yearID.data
        logger.info(f"{session["username"]} requested league info for {lgID}, {year}")

        with db.session.no_autoflush:

            # Get the standings and other info
            standings = get_standings(lgID, year)

            logger.info(f"Standings returned for {lgID}, {year}: {standings}")
            return render_template(
                "league.html",
                form=form,
                lgID=lgID,
                yearID=year,
                standings=standings,
            )

    return render_template("league.html", form=form)


@league_routes.route("/get_years/<lgID>", methods=["GET"])
def get_years(lgID):
    years = LeaguesForm.get_years_for_league(lgID)
    return jsonify({"years": years})


def get_standings(lgID, yearID):
    # Initialize a dictionary to store teams grouped by divID
    standings = {}

    # Query the teams based on lgID and yearID
    teams = (
        db.session.query(Teams)
        .filter(Teams.lgID == lgID, Teams.yearID == yearID)
        .order_by(Teams.team_rank)
        .all()
    )

    # Group teams by divID
    for team in teams:
        divID = team.divID if team.divID is not None else "None"
        if divID not in standings:
            standings[divID] = []
        standings[divID].append(team)

    return standings
