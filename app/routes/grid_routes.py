from flask import Blueprint, flash, redirect, render_template, request, url_for

from app import db

from ..models import People

grid_routes = Blueprint("grid_routes", __name__, template_folder="templates")


def extract_form_data():
    return {
        "prompt1": {
            "prompt1-option": request.form.get("prompt1-option"),
            "prompt1-operator": request.form.get("prompt1-operator"),
            "prompt1-number": request.form.get("prompt1-number"),
            "prompt1-team": request.form.get("prompt1-team"),
        },
        "prompt2": {
            "prompt2-option": request.form.get("prompt2-option"),
            "prompt2-operator": request.form.get("prompt2-operator"),
            "prompt2-number": request.form.get("prompt2-number"),
            "prompt2-team": request.form.get("prompt2-team"),
        },
    }


career_and_season_options = [
    "avg_career",
    "era_career",
    "wins_career",
    "k_career",
    "hits_career",
    "hr_career",
    "save_career",
    "war_career",
    "avg_season",
    "era_season",
    "hr_season",
    "win_season",
    "rbi_season",
    "run_season",
    "hits_season",
    "k_season",
    "hr_sb_season",
    "save_season",
    "war_season",
]


def validate_form_data(form_data):
    errors = []

    # Check required fields
    if not form_data["prompt1"]["prompt1-option"]:
        errors.append("Prompt 1 is required.")
    if not form_data["prompt2"]["prompt2-option"]:
        errors.append("Prompt 2 is required.")

    # Check additional fields for prompt1
    if form_data["prompt1"]["prompt1-option"] in career_and_season_options:
        if not form_data["prompt1"]["prompt1-operator"]:
            errors.append("Operator for Prompt 1 is required.")
        if not form_data["prompt1"]["prompt1-number"]:
            errors.append("Number for Prompt 1 is required.")
    if (
        form_data["prompt1"]["prompt1-option"] == "played_for_team"
        and not form_data["prompt1"]["prompt1-team"]
    ):
        errors.append("Team for Prompt 1 is required.")

    # Check additional fields for prompt2
    if form_data["prompt2"]["prompt2-option"] in career_and_season_options:
        if not form_data["prompt2"]["prompt2-operator"]:
            errors.append("Operator for Prompt 2 is required.")
        if not form_data["prompt2"]["prompt2-number"]:
            errors.append("Number for Prompt 2 is required.")
    if (
        form_data["prompt2"]["prompt2-option"] == "played_for_team"
        and not form_data["prompt2"]["prompt2-team"]
    ):
        errors.append("Team for Prompt 2 is required.")

    return errors


def parse_prompts(form_data, params):
    return


def perform_query(form_data):
    # Get base query
    query = db.session.query(People)

    # Extract parameters from the form data
    params = []
    parse_prompts(form_data, params)

    result = query.first()

    name = f"{result[13]} {result[14]}"

    return name


@grid_routes.route("/", methods=["GET", "POST"])
def get_player():
    if request.method == "POST":
        # Extract form data
        form_data = extract_form_data()

        # Validate form data
        errors = validate_form_data(form_data)
        if errors:
            for error in errors:
                flash(error, "error")

            flash(form_data, "info")
            return render_template("immaculate_grid.html", form_data=form_data)

        # Perform necessary actions with the extracted data
        # For example, query a database or perform calculations
        name = perform_query(form_data)

        # Flash a message or redirect to another page
        flash(name, "info")
        return redirect(url_for("grid_routes.get_player"))

    return render_template("immaculate_grid.html")
