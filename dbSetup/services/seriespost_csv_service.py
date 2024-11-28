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
            counts = {"updated_rows": 0, "new_rows":0,}
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
    finally:
        session.close()

    return counts


def process_row(row, session, counts):
    try:
        entry = SeriesPost(
            yearID=int(row["yearID"]),
            round=(row["round"]),
            teamIDwinner=(row["teamIDwinner"]),
            lgIDwinner=(row["lgIDwinner"]),
            teamIDloser=(row["teamIDloser"]),
            lgIDloser=(row["lgIDloser"]),
            wins=(int(row["wins"]) if row["wins"] else None),
            losses=(int(row["losses"]) if row["losses"] else None),
            ties=(int(row["ties"]) if row["ties"] else None),
        )

        existing_entry = (
            session.query(SeriesPost)
            .filter_by(
                yearID=entry.yearID,
                round=entry.round,
                teamIDwinner=entry.teamIDwinner,
                lgIDwinner=entry.lgIDwinner,
                teamIDloser=entry.teamIDloser,
                lgIDloser=entry.lgIDloser,            
                )
            .first()
        )

        # Check for existing record
        if existing_entry:
            for column in SeriesPost.__table__.columns:
                # Skip the 'ID' column as it should not be modified
                if column.name == 'seriespost_ID':
                    continue

                updated = False
                new_value = getattr(entry, column.name)
                existing_value = getattr(existing_entry, column.name)

                #skip if both columns are null
                if new_value is None and existing_value is None:
                    continue

                # If the values are different, update the existing record
                if existing_value is None or new_value != existing_value :
                    setattr(existing_entry, column.name, new_value)
                    updated = True

            if updated:
                counts["updated_rows"] += 1  # Only count as updated if something changed
        else:
            counts["new_rows"] += 1
            session.add(entry)

    except SQLAlchemyError as e:
        raise RuntimeError(f"Error processing row: {str(e)}")
