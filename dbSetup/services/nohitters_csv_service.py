import csv

import csi3335f2024 as cfg
from models import NoHitters, People, Teams
from utils import create_enginestr_from_values, create_session_from_str, get_csv_path


def upload_nohitters_csv():
    print("Updating nohitters table")
    csv_file_path = get_csv_path("NoHitters.csv")

    if len(csv_file_path) == 0:
        raise FileNotFoundError("Error: NoHitters.csv not found")

    # Process the CSV file
    try:
        result = update_nohitters_from_csv(csv_file_path)
        print(f"File processed successfully: {result}")
    except Exception as e:
        raise RuntimeError(f"Error processing file: {str(e)}")


def update_nohitters_from_csv(file_path):
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

    finally:
        session.close()

    return counts


def process_row(row, session, counts):

    # Get row data
    playerID = row["playerID"]
    yearID = row["yearID"]
    teamID = row["teamID"]
    type = row["type"]
    date = row["date"]

    # Check if playerID exists
    if not session.query(People).filter_by(playerID=playerID).first():
        return
    # Check if teamID exists
    if not session.query(Teams).filter_by(teamID=teamID).first():
        return

    # Check for existing record, skip if found
    if (
        session.query(NoHitters)
        .filter_by(
            playerID=playerID,
            yearID=yearID,
            teamID=teamID,
            type=type,
            date=date,
        )
        .first()
    ):
        counts["skipped_rows"] += 1
    else:
        # Add entry to DB
        entry = NoHitters(
            playerID=playerID,
            teamID=teamID,
            yearID=yearID,
            type=type,
            date=date,
        )
        counts["new_rows"] += 1
        session.add(entry)
