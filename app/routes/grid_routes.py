import logging
import os

import requests
from bs4 import BeautifulSoup
from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from app import db

from ..filters import (
    CareerStatFilter,
    MiscFilter,
    PositionFilter,
    SeasonStatFilter,
    TeamFilter,
)
from ..models import BattingStats, People, PitchingStats
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

    # Check if the second prompt provides a team but the first does not
    if len(params) > 1 and params[0]["team"] is None and params[1]["team"] is not None:
        params.reverse()

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

    result = choose_player(query, returned_player_ids)

    # Parse player info from result
    if result:
        player_name = f"{result.nameFirst} {result.nameLast}"
        debut_year = str(result.debutDate)[:4] if result.debutDate else "Unknown"
        final_year = (
            str(result.finalGameDate)[:4] if result.finalGameDate else "Present"
        )
        player_years = f"{debut_year} - {final_year}"

        # Get the photo and link to the Baseball Reference page
        player_photo = get_baseball_reference_photo(result.playerID)

        player_link = url_for("player_routes.get_player", playerID=result.playerID)

        # Return the players info
        return {
            "player_id": result.playerID,
            "player_name": player_name,
            "player_years": player_years,
            "player_photo": player_photo,
            "player_link": player_link,
        }

    return None


def choose_player(query, returned_player_ids):
    if returned_player_ids:
        query = query.filter(People.playerID.not_in(returned_player_ids))

    # Sort by criteria that indicate "less well-known" players
    # Example: Players with fewer games (G) or plate appearances (PA) in BattingStats
    query1 = query.join(BattingStats).order_by(
        BattingStats.yearID.asc(), BattingStats.b_G.asc(), BattingStats.b_PA.asc()
    )

    player = query1.first()
    if player == None:
        query2 = query.join(PitchingStats).order_by(
            PitchingStats.yearID.asc(), PitchingStats.p_G.asc()
        )
        player = query2.first()

    return player


def get_baseball_reference_photo(player_id):
    # Construct the URL for the player's page on Baseball-Reference
    url = f"https://www.baseball-reference.com/players/{player_id[0]}/{player_id}.shtml"

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
                logger.warning(f"Image not available for {player_id}")
                return None
        else:
            logger.warning(f"Media item div not found for {player_id}")
            return None
    else:
        logger.error(f"Player not found for {player_id}")
        return None


@grid_routes.route("/", methods=["GET", "POST"])
def get_player():

    # Store returned player info
    if "returned_players" not in session:
        session["returned_players"] = []

    # Store the player ids that are returned
    if "returned_player_ids" not in session:
        session["returned_player_ids"] = []

    returned_players = session["returned_players"]
    returned_player_ids = set(session["returned_player_ids"])

    if request.method == "POST":
        # Extract form data
        form_data = extract_form_data(request_form=request.form)

        # Log form data
        username = session.get("username", "Unknown User")

        # Validate form data
        errors = validate_form_data(form_data)
        if errors:
            logger.info(f"Invalid Request: {errors}")
            for error in errors:
                flash(error, "error")

            return render_template(
                "immaculate_grid.html",
                team_mappings=TEAM_MAPPINGS,
                option_groups=OPTION_GROUPS,
                form_data=form_data,
            )

        result = perform_query(form_data, returned_player_ids)

        if result != None:
            # Log output
            logger.info(f"Player Returned: {result["player_name"]}")
            logger.info(f"Years Returned: {result["player_years"]}")

            # Add player info to session info
            returned_players.append(result)
            session["returned_players"] = returned_players

            # Add player to the session ids
            returned_player_ids.add(result["player_id"])
            session["returned_player_ids"] = list(returned_player_ids)
        else:
            flash("No player could be found that meets those criteria", "danger")
        return redirect(url_for("grid_routes.get_player"))

    return render_template(
        "immaculate_grid.html",
        team_mappings=TEAM_MAPPINGS,
        option_groups=OPTION_GROUPS,
        returned_players=returned_players,
    )


@grid_routes.route("/clear_players", methods=["POST"])
def clear_players():
    # Clear the returned_players and returned_player_ids from the session
    session.pop("returned_players", None)
    session.pop("returned_player_ids", None)
    logger.info(f"Clearing results list for {session["username"]}")
    flash("Player list cleared.", "info")
    return redirect(url_for("grid_routes.get_player"))
