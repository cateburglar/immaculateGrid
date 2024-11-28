import csv

from csi3335f2024 import mysql
from models import AllstarFull, Leagues, People
from sqlalchemy.exc import SQLAlchemyError
from utils import create_enginestr_from_values, create_session_from_str, get_csv_path


def upload_allstarfull_csv():
    print("Updating allstarfull table")
    csv_file_path = get_csv_path("AllstarFull.csv")

    if len(csv_file_path) == 0:
        print("Error: AllstarFull.csv not found")
        return

    # Process the CSV file
    try:
        print(update_allstarfull_from_csv(csv_file_path))
        print("File processed successfully")
    except Exception as e:
        print(f"Error: {str(e)}")


def update_allstarfull_from_csv(file_path):
    try:
        with open(file_path, newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            session = create_session_from_str(create_enginestr_from_values(mysql))
            counts = {"updated_rows": 0, "new_rows" : 0}
            # Process rows
            for row in reader:
                process_row(row, session, counts)
            # Commit updates
            session.commit()
    except (csv.Error, SQLAlchemyError) as e:
        session.rollback()
        raise RuntimeError(f"Error updating allstarfull from CSV: {str(e)}")
    except Exception as e:
        raise RuntimeError(f"Unexpected error: {str(e)}")

    return counts


def process_row(row, session, counts):

    try:
        entry = AllstarFull(
            # Convert empty strings to None
            playerID=(row["playerID"]),
            yearID=(row["yearID"]),
            teamID=(row["teamID"]),
            gameID=(row["gameID"] or None),
            lgID=(row["lgID"]),
            GP=(int(row["GP"]) if row["GP"] else None),
            startingPos=(int(row["startingPos"]) if row["startingPos"] else None),
        )

        # Check if playerID exists in the people table
        player_exists = (
            session.query(People).filter_by(playerID=(row["playerID"])).first()
        )

        if not player_exists:
            print(
                f"playerID {row["playerID"]} does not exist in the people table. Skipping row."
            )
            return

        # Check if lgID exists in the leagues table
        lg_exists = session.query(Leagues).filter_by(lgID=row["lgID"]).first()

        if not lg_exists:
            print(
                f"lgID {row["lgID"]} does not exist in the leagues table. Skipping row."
            )
            return
        existing_record = session.query(AllstarFull).filter_by(
                playerID=entry.playerID,
                yearID=entry.yearID,
                teamID=entry.teamID,
                lgID=entry.lgID
            ).first()
        
        # Check for existing record
        if existing_record:
            for column in AllstarFull.__table__.columns:
                # Skip the 'ID' column as it should not be modified
                if column.name == 'allstarfull_ID':
                    continue

                updated = False
                new_value = getattr(entry, column.name)
                existing_value = getattr(existing_record, column.name)

                #skip if both columns are null
                if new_value is None and existing_value is None:
                    continue

                # If the values are different, update the existing record
                if existing_value is None or new_value != existing_value :
                    setattr(existing_record, column.name, new_value)
                    updated = True

                if updated:
                    counts["updated_rows"] += 1 # Only count as updated if something changed
        else:
            counts["new_rows"] += 1
            session.add(entry)

    except SQLAlchemyError as e:
        raise RuntimeError(f"Error processing row: {str(e)}")
