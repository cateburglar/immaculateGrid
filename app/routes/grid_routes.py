from flask import Blueprint, flash, redirect, render_template, request, url_for
from sqlalchemy.orm import aliased

from app import db

from ..filters import (
    CareerStatFilter,
    MiscFilter,
    PositionFilter,
    SeasonStatFilter,
    TeamFilter,
)
from ..models import Appearances, People, Teams
from ..static.constants import OPTION_GROUPS, TEAM_MAPPINGS
from ..utils import extract_form_data, parse_prompts, validate_form_data

grid_routes = Blueprint("grid_routes", __name__, template_folder="templates")


def perform_query(form_data):
    # Get base query
    query = db.session.query(People)

    # Extract parameters from the form data
    params = parse_prompts(form_data)

    flash(params, "info")

    # Apply filters based on the form data
    team = None
    for i, param in enumerate(params):
        option = param["option"]
        operator = param["operator"]
        number = param["number"]
        team = param["team"]

        if option in OPTION_GROUPS["Career Options"].keys():
            query = CareerStatFilter(
                query, option, operator, float(number), team
            ).apply()
        elif option in OPTION_GROUPS["Season Options"].keys():
            query = SeasonStatFilter(
                query, option, operator, float(number), team
            ).apply()
        elif option == "played_for_team":
            query = TeamFilter(query, team, i).apply()
        elif option in OPTION_GROUPS["Position Options"]:
            query = PositionFilter(query, option, team).apply()
        else:
            query = MiscFilter(query, option, team).apply()

    result = query.first()

    if result:
        player_name = f"{result.nameFirst} {result.nameLast}"
        return player_name

    return None


@grid_routes.route("/", methods=["GET", "POST"])
def get_player():
    if request.method == "POST":
        # Extract form data
        form_data = extract_form_data(request_form=request.form)

        # Validate form data
        errors = validate_form_data(form_data)
        if errors:
            for error in errors:
                flash(error, "error")

            flash(form_data, "info")
            return render_template(
                "immaculate_grid.html",
                team_mappings=TEAM_MAPPINGS,
                option_groups=OPTION_GROUPS,
                form_data=form_data,
            )

        name = perform_query(form_data)

        flash(form_data, "info")
        flash(name, "success")
        return redirect(url_for("grid_routes.get_player"))

    return render_template(
        "immaculate_grid.html", team_mappings=TEAM_MAPPINGS, option_groups=OPTION_GROUPS
    )
