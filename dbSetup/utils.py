import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


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


def create_session_from_str(enginestr):
    try:
        # Creates a Session from an engine string
        engine = create_engine(enginestr)
        Session = sessionmaker(bind=engine)
        return Session()
    except Exception as e:
        print(f"Error creating session: {e}")
        return None
