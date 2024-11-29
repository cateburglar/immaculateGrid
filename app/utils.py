import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .static.constants import OPTION_GROUPS, TEAM_MAPPINGS


def model_to_dict(model):
    """
    Convert a SQLAlchemy model instance to a dictionary.
    """
    return {
        column.name: getattr(model, column.name) for column in model.__table__.columns
    }


def get_csv_path(filename):
    # Define the path to the CSV file
    base_dir = os.path.abspath(os.path.dirname(__file__))
    csv_file_path = os.path.join(base_dir, "static", "csv", filename)

    # Check if the file exists
    if not os.path.exists(csv_file_path):
        return ""

    return csv_file_path


def create_enginestr_from_values(mysql):
    # Create engine from dictionary values
    return (
        "mysql+pymysql://"
        + mysql["user"]
        + ":"
        + mysql["password"]
        + "@"
        + mysql["host"]
        + "/"
        + mysql["db"]
    )


def create_session_from_str(enginestr):
    try:
        # Creates a Session from an engine string
        engine = create_engine(enginestr)
        Session = sessionmaker(bind=engine)
        return Session()
    except Exception as e:
        print(f"Error creating session: {e}")
        return None


def extract_form_data(request_form):
    return {
        "prompt1": {
            "prompt1-option": request_form.get("prompt1-option"),
            "prompt1-number": request_form.get("prompt1-number"),
            "prompt1-team": request_form.get("prompt1-team"),
        },
        "prompt2": {
            "prompt2-option": request_form.get("prompt2-option"),
            "prompt2-number": request_form.get("prompt2-number"),
            "prompt2-team": request_form.get("prompt2-team"),
        },
    }


def validate_form_data(form_data):
    errors = []

    # Check required fields
    if not form_data["prompt1"]["prompt1-option"]:
        errors.append("Prompt 1 is required.")
    if not form_data["prompt2"]["prompt2-option"]:
        errors.append("Prompt 2 is required.")

    # Check additional fields for prompt1
    if (
        form_data["prompt1"]["prompt1-option"] in OPTION_GROUPS["Career Options"].keys()
        or form_data["prompt1"]["prompt1-option"]
        in OPTION_GROUPS["Season Options"].keys()
    ):
        if not form_data["prompt1"]["prompt1-number"]:
            errors.append("Number for Prompt 1 is required.")
    if (
        form_data["prompt1"]["prompt1-option"] == "played_for_team"
        and not form_data["prompt1"]["prompt1-team"]
    ):
        errors.append("Team for Prompt 1 is required.")

    # Check additional fields for prompt2
    if (
        form_data["prompt2"]["prompt2-option"] in OPTION_GROUPS["Career Options"].keys()
        or form_data["prompt2"]["prompt2-option"]
        in OPTION_GROUPS["Season Options"].keys()
    ):
        if not form_data["prompt2"]["prompt2-number"]:
            errors.append("Number for Prompt 2 is required.")
    if (
        form_data["prompt2"]["prompt2-option"] == "played_for_team"
        and not form_data["prompt2"]["prompt2-team"]
    ):
        errors.append("Team for Prompt 2 is required.")

    return errors


# Returns an array of two dictionaries, one for each prompt
def parse_prompts(form_data):
    params = []
    if form_data["prompt1"]:
        params.append(
            {
                "option": form_data["prompt1"]["prompt1-option"],
                "number": form_data["prompt1"]["prompt1-number"],
                "team": form_data["prompt1"]["prompt1-team"],
            }
        )

    if form_data["prompt2"]:
        params.append(
            {
                "option": form_data["prompt2"]["prompt2-option"],
                "number": form_data["prompt2"]["prompt2-number"],
                "team": form_data["prompt2"]["prompt2-team"],
            }
        )

    return params
