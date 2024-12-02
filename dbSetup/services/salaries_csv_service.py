import csv

from csi3335f2024 import mysql
from models import People, Teams, Salaries
from sqlalchemy.exc import SQLAlchemyError
from utils import create_enginestr_from_values, create_session_from_str, get_csv_path


def upload_salaries_csv():
    print("Updating salaries table")
    csv_file_path = get_csv_path("Salaries.csv")

    if len(csv_file_path) == 0:
        print("Error: Pitching.csv not found")
        return

    # Process the CSV file
    try:
        print(update_salaries_from_csv(csv_file_path))
        print("File processed successfully")
    except Exception as e:
        print(f"Error: {str(e)}")

def update_salaries_from_csv(file_path):
    try:
        with open(file_path, newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            session = create_session_from_str(create_enginestr_from_values(mysql))
            counts = {"new_rows": 0, "updated_rows": 0, "peopleNotExist": 0, "teamNotExist": 0}

            # Process rows
            for row in reader:
                process_salary_row(row, session, counts)

            # Commit updates
            session.commit()
    except (csv.Error, SQLAlchemyError) as e:
        session.rollback()
        raise RuntimeError(f"Error updating salaries from CSV: {str(e)}")
    except Exception as e:
        raise RuntimeError(f"Unexpected error: {str(e)}")

    return counts


def process_salary_row(row, session, counts):
    try:
        salaries_record = Salaries(
            playerID=row['playerID'],
            yearId=int(row['yearID']),
            teamID=row['teamID'],
            salary=float(row['salary']) if row['salary'] else None,
        )

        # Check if playerID exists in the people table
        player_exists = session.query(People).filter_by(playerID=salaries_record.playerID).first()
        if not player_exists:
            counts["peopleNotExist"] += 1
            print(f"playerID {salaries_record.playerID} does not exist in the people table. Skipping row.")
            return

        # Check if teamID exists in teams table
        team_exists = session.query(Teams).filter_by(teamID=salaries_record.teamID).first()
        if not team_exists:
            counts["teamNotExist"] += 1
            print(f"teamID {salaries_record.teamID} does not exist in the teams table. Skipping row.")
            return

        # Check if a row with the same playerID, yearId, and teamID exists
        existing_entry = (
            session.query(Salaries)
            .filter_by(
                playerID=salaries_record.playerID,
                yearId=salaries_record.yearId,
                teamID=salaries_record.teamID,
            )
            .first()
        )

        if existing_entry:
            updated = False
            for column in Salaries.__table__.columns:
                if column.name == 'salaries_ID':
                    continue

                new_value = getattr(salaries_record, column.name)
                existing_value = getattr(existing_entry, column.name)

                # Skip if both columns are null
                if new_value is None and existing_value is None:
                    continue

                # If the values are different, update the existing record
                if existing_value is None or new_value != existing_value:
                    setattr(existing_entry, column.name, new_value)
                    updated = True

            if updated:
                counts["updated_rows"] += 1  # Only count as updated if something changed
        else:
            counts["new_rows"] += 1
            session.add(salaries_record)

    except SQLAlchemyError as e:
        raise RuntimeError(f"Error processing salary row: {str(e)}")

