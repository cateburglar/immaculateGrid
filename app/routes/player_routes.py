import logging
import os

import requests
from bs4 import BeautifulSoup
from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from sqlalchemy import desc

from app import db

from ..models import Appearances, Awards, BattingStats, People, PitchingStats

# Ensure the logging directory exists
log_dir = os.path.join("app", "logging")
os.makedirs(log_dir, exist_ok=True)

# Configure custom logger
log_file_path = os.path.join(log_dir, "player_logs.log")
logger = logging.getLogger("player_routes_logger")
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler(log_file_path)
formatter = logging.Formatter("%(asctime)s - %(message)s")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

player_routes = Blueprint("player_routes", __name__, template_folder="templates")


@player_routes.route("/<playerID>", methods=["GET"])
def get_player(playerID):

    # Get the team name based on the year and ID
    player = db.session.query(People).filter(People.playerID == playerID).first()

    # Redirect back to home page if no player is found
    if player == None:
        return redirect(url_for("home_routes.home"))

    # Get the players historic info
    awards = get_awards(playerID)
    appearances = get_appearances(playerID)
    batting_stats = get_season_batting_stats(playerID)
    pitching_stats = get_seaason_pitching_stats(playerID)

    # Check and modify the finalGameDate
    current = "2022-05-15"
    if player.finalGameDate and player.finalGameDate.strftime("%Y-%m-%d") == current:
        player.finalGameDate = None

    # Scrape the photo
    photo = get_baseball_reference_photo(playerID)
    link = None
    if photo:
        link = (
            f"https://www.baseball-reference.com/players/{playerID[0]}/{playerID}.shtml"
        )

    return render_template(
        "player.html",
        photo=photo,
        link=link,
        player=player,
        awards=awards,
        appearances=appearances,
        batting_stats=batting_stats,
        pitching_stats=pitching_stats,
    )


def get_awards(playerID):
    return (
        db.session.query(Awards)
        .filter(Awards.playerID == playerID)
        .order_by(desc(Awards.yearID))
        .all()
    )


def get_appearances(playerID):
    return (
        db.session.query(Appearances)
        .filter(Appearances.playerID == playerID)
        .order_by(desc(Appearances.yearID))
        .all()
    )


def get_season_batting_stats(playerID):
    return (
        db.session.query(BattingStats)
        .filter(BattingStats.playerID == playerID)
        .order_by(desc(BattingStats.yearID))
        .all()
    )


def get_seaason_pitching_stats(playerID):
    return (
        db.session.query(PitchingStats)
        .filter(PitchingStats.playerID == playerID)
        .order_by(desc(PitchingStats.yearID))
        .all()
    )


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
