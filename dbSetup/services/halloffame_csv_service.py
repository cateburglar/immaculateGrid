import csv

import csi3335f2024 as cfg
from models import HallofFame, People
from utils import create_enginestr_from_values, create_session_from_str, get_csv_path


def upload_halloffame_csv():
    print("Updating halloffame table")
    csv_file_path = get_csv_path("HallOfFame.csv")

    if len(csv_file_path) == 0:
        raise FileNotFoundError("Error: HallOfFame.csv not found")

    # Process the CSV file
    try:
        result = update_halloffame_from_csv(csv_file_path)
        print(f"File processed successfully: {result}")
    except Exception as e:
        raise RuntimeError(f"Error processing file: {str(e)}")


def update_halloffame_from_csv(file_path):
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
    yearID = int(row["yearid"])
    votedBy = row["votedBy"]
    ballots = int(row["ballots"]) if row["ballots"] else None
    needed = int(row["needed"]) if row["needed"] else None
    votes = int(row["votes"]) if row["votes"] else None
    inducted = row["inducted"] if row["inducted"] else None
    category = row["category"] if row["category"] else None
    note = row["needed_note"] if row["needed_note"] else None

    # Check if playerID exists
    if not session.query(People).filter_by(playerID=playerID).first():
        return

    # Check for existing record, skip if found
    if (
        session.query(HallofFame)
        .filter_by(playerID=playerID, yearID=yearID, votedBy=votedBy)
        .first()
    ):
        counts["skipped_rows"] += 1
    else:
        # Add entry to DB
        entry = HallofFame(
            playerID=playerID,
            yearID=yearID,
            votedBy=votedBy,
            ballots=ballots,
            needed=needed,
            votes=votes,
            inducted=inducted,
            category=category,
            note=note,
        )
        counts["new_rows"] += 1
        session.add(entry)
