import csv

from csi3335f2024 import mysql
from models import SeriesPost
from sqlalchemy.exc import SQLAlchemyError
from utils import create_enginestr_from_values, create_session_from_str, get_csv_path


def upload_seriespost_csv():
    print("Updating seriespost table")
    csv_file_path = get_csv_path("SeriesPost.csv")

    if len(csv_file_path) == 0:
        raise FileNotFoundError("Error: SeriesPost.csv not found")

    # Process the CSV file
    try:
        result = update_seriespost_from_csv(csv_file_path)
        print(f"File processed successfully: {result}")
    except Exception as e:
        raise RuntimeError(f"Error processing file: {str(e)}")


def update_seriespost_from_csv(file_path):
    try:
        with open(file_path, newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            session = create_session_from_str(create_enginestr_from_values(mysql))
            counts = {"updated_rows": 0}
            # Process rows
            for row in reader:
                process_row(row, session, counts)
            # Commit updates
            session.commit()
    except (csv.Error, SQLAlchemyError) as e:
        session.rollback()
        raise RuntimeError(f"Error updating seriespost from CSV: {str(e)}")
    except Exception as e:
        raise RuntimeError(f"Unexpected error: {str(e)}")

    return counts


def process_row(row, session, counts):
    try:
        entry = SeriesPost(
            yearID=(int(row["yearID"]) if row["yearID"] else None),
            round=(row["round"] or None),
            teamIDwinner=(row["teamIDwinner"] or None),
            lgIDwinner=(row["lgIDwinner"] or None),
            teamIDloser=(row["teamIDloser"] or None),
            lgIDloser=(row["lgIDloser"] or None),
            wins=(int(row["wins"]) if row["wins"] else None),
            losses=(int(row["losses"]) if row["losses"] else None),
            ties=(int(row["ties"]) if row["ties"] else None),
        )

        session.merge(entry)
        counts["updated_rows"] += 1
    except SQLAlchemyError as e:
        raise RuntimeError(f"Error processing row: {str(e)}")
