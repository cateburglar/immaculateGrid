import csv

import csi3335f2024 as cfg
from models import People
from utils import create_enginestr_from_values, create_session_from_str, get_csv_path


def upload_people_csv():
    print("Updating people table")
    csv_file_path = get_csv_path("People.csv")

    if len(csv_file_path) == 0:
        print("Error: People.csv not found")
        return

    # Process the CSV file
    try:
        print(update_people_from_csv(csv_file_path))
        print("File processed successfully")
    except Exception as e:
        print(f"Error: {str(e)}")


def update_people_from_csv(file_path):
    with open(file_path, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        new_rows = 0
        updated_rows = 0

        # Create session
        session = create_session_from_str(create_enginestr_from_values(mysql=cfg.mysql))

        for row in reader:
            # Convert empty strings to None
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

            # Debug prints
            # print(f"Processing row: playerID={playerID}")

            # Check if playerID exists in the people table
            player_exists = session.query(People).filter_by(playerID=playerID).first()

            if player_exists:
                # Update the existing record
                player_exists.birthYear = birthYear
                player_exists.birthMonth = birthMonth
                player_exists.birthDay = birthDay
                player_exists.birthCity = birthCity
                player_exists.birthCountry = birthCountry
                player_exists.birthState = birthState
                player_exists.deathYear = deathYear
                player_exists.deathMonth = deathMonth
                player_exists.deathDay = deathDay
                player_exists.deathCountry = deathCountry
                player_exists.deathState = deathState
                player_exists.deathCity = deathCity
                player_exists.nameFirst = nameFirst
                player_exists.nameLast = nameLast
                player_exists.nameGiven = nameGiven
                player_exists.weight = weight
                player_exists.height = height
                player_exists.bats = bats
                player_exists.throws = throws
                player_exists.debutDate = debutDate
                player_exists.finalGameDate = finalGameDate
                updated_rows += 1
            else:
                # Insert a new record
                new_entry = People(
                    playerID=playerID,
                    birthYear=birthYear,
                    birthMonth=birthMonth,
                    birthDay=birthDay,
                    birthCity=birthCity,
                    birthCountry=birthCountry,
                    birthState=birthState,
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
                new_rows += 1

            session.commit()

    session.close()
    return {"new_rows": new_rows, "updated_rows": updated_rows}
