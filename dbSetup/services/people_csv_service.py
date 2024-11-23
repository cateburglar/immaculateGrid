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
            counts = {"updated_rows": 0, "new_rows": 0}
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
        playerID = row["playerID"]
        birthYear = row["birthYear"] or None
        birthMonth = row["birthMonth"] or None
        birthDay = row["birthDay"] or None
        birthCity = row["birthCity"] or None
        birthCountry = row["birthCountry"] or None
        birthState = row["birthState"] or None
        deathYear = row["deathYear"] or None
        deathMonth = row["deathMonth"] or None
        deathDay = row["deathDay"] or None
        deathCountry = row["deathCountry"] or None
        deathState = row["deathState"] or None
        deathCity = row["deathCity"] or None
        nameFirst = row["nameFirst"] or None
        nameLast = row["nameLast"] or None
        nameGiven = row["nameGiven"] or None
        weight = int(row["weight"]) if row["weight"] else None
        height = int(row["height"]) if row["height"] else None
        bats = row["bats"] or None
        throws = row["throws"] or None
        debutDate = row["debut"] or None
        finalGameDate = row["finalGame"] or None

        # Check if a row with the same playerID exists
        existing_entry = session.query(People).filter_by(playerID=playerID).first()

        if existing_entry:
            existing_entry.birthYear = birthYear
            existing_entry.birthMonth = birthMonth
            existing_entry.birthDay = birthDay
            existing_entry.birthCountry = birthCountry
            existing_entry.birthState = birthState
            existing_entry.birthCity = birthCity
            existing_entry.deathYear = deathYear
            existing_entry.deathMonth = deathMonth
            existing_entry.deathDay = deathDay
            existing_entry.deathCountry = deathCountry
            existing_entry.deathState = deathState
            existing_entry.deathCity = deathCity
            existing_entry.nameFirst = nameFirst
            existing_entry.nameLast = nameLast
            existing_entry.nameGiven = nameGiven
            existing_entry.weight = weight
            existing_entry.height = height
            existing_entry.bats = bats
            existing_entry.throws = throws
            existing_entry.debutDate = debutDate
            existing_entry.finalGameDate = finalGameDate
            counts["updated_rows"] += 1
        else:
            # Insert a new record
            new_entry = People(
                playerID=playerID,
                birthYear=birthYear,
                birthMonth=birthMonth,
                birthDay=birthDay,
                birthCountry=birthCountry,
                birthState=birthState,
                birthCity=birthCity,
                deathYear=deathYear,
                deathMonth=deathMonth,
                deathDay=deathDay,
                deathCountry=deathCountry,
                deathState=deathState,
                deathCity=deathCity,
                nameFirst=nameFirst,
                nameLast=nameLast,
                nameGiven=nameGiven,
                weight=weight,
                height=height,
                bats=bats,
                throws=throws,
                debutDate=debutDate,
                finalGameDate=finalGameDate,
            )
            session.add(new_entry)
            counts["new_rows"] += 1
    except SQLAlchemyError as e:
        raise RuntimeError(f"Error processing row: {str(e)}")
