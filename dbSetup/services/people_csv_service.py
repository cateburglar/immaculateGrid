import csv

from csi3335f2024 import mysql
from models import People
from sqlalchemy.exc import SQLAlchemyError
from utils import create_enginestr_from_values, create_session_from_str, get_csv_path


def upload_people_csv():
    print("Updating people table")
    csv_file_path = get_csv_path("People.csv")

    if len(csv_file_path) == 0:
        raise FileNotFoundError("Error: People.csv not found")

    # Process the CSV file
    try:
        result = update_people_from_csv(csv_file_path)
        print(f"File processed successfully: {result}")
    except Exception as e:
        raise RuntimeError(f"Error processing file: {str(e)}")


def update_people_from_csv(file_path):
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
        raise RuntimeError(f"Error updating people from CSV: {str(e)}")
    except Exception as e:
        raise RuntimeError(f"Unexpected error: {str(e)}")

    return counts


def process_row(row, session, counts):
    try:
        person = People(
            playerID=row["playerID"],
            birthYear=(row["birthYear"] or None),
            birthMonth=(row["birthMonth"] or None),
            birthDay=(row["birthDay"] or None),
            birthCity=(row["birthCity"] or None),
            birthCountry=(row["birthCountry"] or None),
            birthState=(row["birthState"] or None),
            deathYear=(row["deathYear"] or None),
            deathMonth=(row["deathMonth"] or None),
            deathDay=(row["deathDay"] or None),
            deathCountry=(row["deathCountry"] or None),
            deathState=(row["deathState"] or None),
            deathCity=(row["deathCity"] or None),
            nameFirst=(row["nameFirst"] or None),
            nameLast=(row["nameLast"] or None),
            nameGiven=(row["nameGiven"] or None),
            weight=(int(row["weight"]) if row["weight"] else None),
            height=(int(row["height"]) if row["height"] else None),
            bats=(row["bats"] or None),
            throws=(row["throws"] or None),
            debutDate=(row["debut"] or None),
            finalGameDate=(row["finalGame"] or None),
        )
        counts["updated_rows"] += 1
        session.merge(person)  # Upsert row
    except SQLAlchemyError as e:
        raise RuntimeError(f"Error processing row: {str(e)}")
