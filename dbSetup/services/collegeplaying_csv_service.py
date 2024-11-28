import csv
from csi3335f2024 import mysql
from models import CollegePlaying, People, Schools
from sqlalchemy.exc import SQLAlchemyError
from utils import create_enginestr_from_values, create_session_from_str, get_csv_path


def upload_collegeplaying_csv():
    print("Updating collegeplaying table")
    csv_file_path = get_csv_path("CollegePlaying.csv")

    if len(csv_file_path) == 0:
        raise FileNotFoundError("Error: CollegePlaying.csv not found")

    # Process the CSV file
    try:
        result = update_collegeplaying_from_csv(csv_file_path)
        print(f"File processed successfully: {result}")
    except Exception as e:
        raise RuntimeError(f"Error processing file: {str(e)}")


def update_collegeplaying_from_csv(file_path):
    try:
        with open(file_path, newline="") as csvfile:
            reader = csv.reader(csvfile)
            session = create_session_from_str(create_enginestr_from_values(mysql))
            counts = {"updated_rows": 0, "new_rows": 0}
            
            # Skip header row if present
            next(reader)

            # Process rows
            for row in reader:
                process_row(row, session, counts)
            # Commit updates
            session.commit()
    except (csv.Error, SQLAlchemyError) as e:
        session.rollback()
        raise RuntimeError(f"Error updating collegeplaying from CSV: {str(e)}")
    except Exception as e:
        raise RuntimeError(f"Unexpected error: {str(e)}")
    finally:
        session.close()
        
    return counts


def process_row(row, session, counts):
    try:
        playerID = row[0] or None
        schoolID = row[1] or None
        yearID = row[2] or None

        # Check if the player exists
        player = session.query(People).filter_by(playerID=playerID).first()
        if not player:
            raise ValueError(f"Player with playerID {playerID} not found")

        # Check if the school exists
        school = session.query(Schools).filter_by(schoolId=schoolID).first()
        if not school:
            raise ValueError(f"School with schoolID {schoolID} not found")

        collegeplaying_record = CollegePlaying(
            playerID=row[0],
            schoolID=row[1],
            yearID=row[2],
        )

        # Check if the row already exists in the collegeplaying table
        existing_entry = (
            session.query(CollegePlaying)
            .filter_by(
                playerID=playerID,
                schoolID=schoolID,
                yearID=yearID
            )
            .first()
        )

        # Check for existing record
        if existing_entry:
            for column in CollegePlaying.__table__.columns:
                # Skip the 'ID' column as it should not be modified
                if column.name == 'collegeplaying_ID':
                    continue

                updated = False
                new_value = getattr(collegeplaying_record, column.name)
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
            session.add(collegeplaying_record)

    except SQLAlchemyError as e:
        raise RuntimeError(f"Error processing row: {str(e)}")
    except ValueError as e:
        print(f"Skipping row due to error: {str(e)}")

