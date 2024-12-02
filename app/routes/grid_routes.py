import logging
import os

from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from app import db

from ..filters import (
    CareerStatFilter,
    MiscFilter,
    PositionFilter,
    SeasonStatFilter,
    TeamFilter,
)
from ..models import People
from ..static.constants import OPTION_GROUPS, TEAM_MAPPINGS
from ..utils import extract_form_data, parse_prompts, validate_form_data

# Ensure the logging directory exists
log_dir = os.path.join("app", "logging")
os.makedirs(log_dir, exist_ok=True)

# Configure custom logger
log_file_path = os.path.join(log_dir, "grid_logs.log")
logger = logging.getLogger("grid_routes_logger")
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler(log_file_path)
formatter = logging.Formatter("%(asctime)s - %(message)s")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

grid_routes = Blueprint("grid_routes", __name__, template_folder="templates")


def perform_query(form_data, returned_player_ids):
    # Get base query
    query = db.session.query(People)

    # Extract parameters from the form data
    params = parse_prompts(form_data)

    flash(params, "info")

    # Apply filters based on the form data
    team = None
    for i, param in enumerate(params):
        option = param["option"]
        number = param["number"]
        if param["team"] != None:
            team = param["team"]

        if option in OPTION_GROUPS["Career Options"].keys():
            query = CareerStatFilter(query, option, float(number), team, i).apply()
        elif option in OPTION_GROUPS["Season Options"].keys():
            query = SeasonStatFilter(query, option, float(number), team, i).apply()
        elif option == "played_for_team":
            query = TeamFilter(query, team, i).apply()
        elif option in OPTION_GROUPS["Position Options"]:
            query = PositionFilter(query, option, team, i).apply()
        else:
            query = MiscFilter(query, option, team, i).apply()

    if returned_player_ids:
        query = query.filter(People.playerID.not_in(returned_player_ids))

    result = query.first()

    if result:
        player_name = f"{result.nameFirst} {result.nameLast}"
        debut_year = str(result.debutDate)[:4] if result.debutDate else "Unknown"
        final_year = (
            str(result.finalGameDate)[:4] if result.finalGameDate else "Present"
        )
        player_years = f"{debut_year} - {final_year}"
        return {
            "player_id": result.playerID,
            "player_name": player_name,
            "player_years": player_years,
        }

    return None


@grid_routes.route("/", methods=["GET", "POST"])
def get_player():
    # Store the player ids that are returned
    if "returned_player_ids" not in session:
        session["returned_player_ids"] = []

    returned_player_ids = set(session["returned_player_ids"])

    if request.method == "POST":
        # Extract form data
        form_data = extract_form_data(request_form=request.form)

        # Log form data
        username = session.get("username", "Unknown User")
        logger.info(f"User {username} Form Data: {form_data}")

        # Validate form data
        errors = validate_form_data(form_data)
        if errors:
            logger.info(f"Invalid Request: {errors}")
            for error in errors:
                flash(error, "error")

            flash(form_data, "info")
            return render_template(
                "immaculate_grid.html",
                team_mappings=TEAM_MAPPINGS,
                option_groups=OPTION_GROUPS,
                form_data=form_data,
            )

        result = perform_query(form_data, returned_player_ids)

        if result != None:
            logger.info(f"Player Returned: {result["player_name"]}")
            logger.info(f"Years Returned: {result["player_years"]}")
            flash(result["player_name"], "success")
            flash(result["player_years"], "success")
            # Add player to the session ids
            returned_player_ids.add(result["player_id"])
            session["returned_player_ids"] = list(returned_player_ids)
        else:
            flash("No player could be found that meets those criteria", "error")
        return redirect(url_for("grid_routes.get_player"))

    return render_template(
        "immaculate_grid.html", team_mappings=TEAM_MAPPINGS, option_groups=OPTION_GROUPS
    )
