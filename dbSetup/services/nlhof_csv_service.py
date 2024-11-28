import csv

import csi3335f2024 as cfg
from models import People
from utils import create_enginestr_from_values, create_session_from_str, get_csv_path


def upload_nlhof_csv():
    print("Updating people table for nl_hof")
    csv_file_path = get_csv_path("NegroLeaguePlayers.csv")

    if len(csv_file_path) == 0:
        raise FileNotFoundError("Error: NegroLeaguePlayers.csv not found")

    # Process the CSV file
    try:
        result = update_nlhof_from_csv(csv_file_path)
        print(f"File processed successfully: {result}")
    except Exception as e:
        raise RuntimeError(f"Error processing file: {str(e)}")


def update_nlhof_from_csv(file_path):
    counts = {"updated_rows": 0, "skipped_rows": 0}
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

    # Check if playerID exists
    if not session.query(People).filter_by(playerID=playerID).first():
        return

    # Check for existing record, skip if found
    record = session.query(People).filter_by(playerID=playerID).first()

    # Modify player to have nl_hof status
    if record:
        record.nl_hof = True
        session.add(record)
        counts["updated_rows"] += 1
    # Skip rows where playerID is not found
    else:
        counts["skipped_rows"] += 1
