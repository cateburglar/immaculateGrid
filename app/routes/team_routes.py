import logging
import os

import requests
from bs4 import BeautifulSoup
from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from sqlalchemy import desc, or_

from app import db

from ..models import Managers, People, SeriesPost, Teams

# Ensure the logging directory exists
log_dir = os.path.join("app", "logging")
os.makedirs(log_dir, exist_ok=True)

# Configure custom logger
log_file_path = os.path.join(log_dir, "teams_logs.log")
logger = logging.getLogger("team_routes_logger")
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler(log_file_path)
formatter = logging.Formatter("%(asctime)s - %(message)s")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

team_routes = Blueprint("team_routes", __name__, template_folder="templates")


@team_routes.route("/<teamID>/<yearID>", methods=["GET"])
def get_team(teamID, yearID):

    # Get the team name based on the year and ID
    team = (
        db.session.query(Teams)
        .filter(Teams.teamID == teamID, Teams.yearID == yearID)
        .first()
    )

    # Redirect back to home page if no team is found
    if team == None:
        return redirect(url_for("home_routes.home"))

    team_name = team.team_name

    # Get the teams historic info
    managers = get_managers(teamID)
    stats = get_team_stats(teamID)
    series_post = get_series_post(teamID)

    # Scrape the photo
    photo = get_baseball_reference_photo(teamID, yearID)

    return render_template(
        "team.html",
        teamID=teamID,
        team_name=team_name,
        photo=photo,
        managers=managers,
        stats=stats,
        series_post=series_post,
    )


def get_team_stats(teamID):
    return (
        db.session.query(Teams)
        .filter(Teams.teamID == teamID)
        .order_by(desc(Teams.yearID))
        .all()
    )


def get_managers(teamID):
    managers_list = (
        db.session.query(Managers)
        .filter(Managers.teamID == teamID)
        .order_by(desc(Managers.yearID))
        .all()
    )

    mapper = []

    for manager in managers_list:
        # Set the playerID to their name for displaying
        name = (
            db.session.query(People.nameGiven)
            .filter(People.playerID == manager.playerID)
            .first()
        )
        if name:
            name = name[0]
        mapper.append({"manager": manager, "name": name})

    return mapper


def get_series_post(teamID):
    return (
        db.session.query(SeriesPost)
        .filter(
            or_(SeriesPost.teamIDloser == teamID, SeriesPost.teamIDwinner == teamID)
        )
        .order_by(desc(SeriesPost.yearID))
        .all()
    )


def get_baseball_reference_photo(teamID, yearID):
    # Construct the URL for the teams page on Baseball-Reference
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
                logger.warning(f"Image not available for {teamID}")
                return None
        else:
            logger.warning(f"Media item div not found for {teamID}")
            return None
    else:
        logger.error(f"Team not found for {teamID}")
        return None
