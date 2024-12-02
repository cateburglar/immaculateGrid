import csv

import csi3335f2024 as cfg
from models import SeasonWarLeaders, People
from utils import create_enginestr_from_values, create_session_from_str, get_csv_path


def upload_seasonwarleaders_csv():
    print("Updating seasonwarleaders table")
    csv_file_path = get_csv_path("SeasonWAR.csv")

    if len(csv_file_path) == 0:
        raise FileNotFoundError("Error: SeasonWAR.csv not found")

    # Process the CSV file
    try:
        result = update_seasonwarleaders_from_csv(csv_file_path)
        print(f"File processed successfully: {result}")
    except Exception as e:
        raise RuntimeError(f"Error processing file: {str(e)}")


def update_seasonwarleaders_from_csv(file_path):
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
    war = row["WAR"]
    year = row["Year"]

    # Check if playerID exists
    if not session.query(People).filter_by(playerID=playerID).first():
        print(f"Player not found: {playerID}")
        counts["skipped_rows"] += 1
        return

    # Check for existing record, skip if found
    if (
        session.query(SeasonWarLeaders)
        .filter_by(
            playerID=playerID,
            war=war,
            yearID=year,
        )
        .first()
    ):
        counts["skipped_rows"] += 1
    # Add new row
    else:
        entry = SeasonWarLeaders(
            playerID=playerID,
            war=war,
            yearID = year,
        )
        counts["new_rows"] += 1
        session.add(entry)
