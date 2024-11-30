import csv

import csi3335f2024 as cfg
from models import CareerWarLeaders, People
from utils import create_enginestr_from_values, create_session_from_str, get_csv_path


def upload_careerwarleaders_csv():
    print("Updating careerwarleaders table")
    csv_file_path = get_csv_path("CareerWAR.csv")

    if len(csv_file_path) == 0:
        raise FileNotFoundError("Error: CareerWAR.csv not found")

    # Process the CSV file
    try:
        result = update_careerwarleaders_from_csv(csv_file_path)
        print(f"File processed successfully: {result}")
    except Exception as e:
        raise RuntimeError(f"Error processing file: {str(e)}")


def update_careerwarleaders_from_csv(file_path):
    counts = {"new_rows": 0, "skipped_rows": 0}
    try:
        with open(file_path, newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            session = create_session_from_str(create_enginestr_from_values(cfg.mysql))

            for row in reader:
                process_row(row, session, counts)

            session.commit()

    except Exception as e:
        session.rollback()
        raise RuntimeError(f"Unexpected error: {str(e)}")

    return counts


def process_row(row, session, counts):

    # Get row data
    playerID = row["playerID"]
    war = row["war"]

    # Check if playerID exists
    if not session.query(People).filter_by(playerID=playerID).first():
        print(f"Player not found: {playerID}")
        counts["skipped_rows"] += 1
        return

    # Check for existing record, skip if found
    if (
        session.query(CareerWarLeaders)
        .filter_by(
            playerID=playerID,
            war=war,
        )
        .first()
    ):
        counts["skipped_rows"] += 1
    # Add new row
    else:
        entry = CareerWarLeaders(
            playerID=playerID,
            war=war,
        )
        counts["new_rows"] += 1
        session.add(entry)
