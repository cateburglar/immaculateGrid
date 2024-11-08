import csv

import dbSetup.csi3335f2024 as cfg
from dbSetup.models import AllstarFull, Leagues, People
from dbSetup.utils import create_enginestr_from_values, create_session_from_str, get_csv_path


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
    with open(file_path, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        new_rows = 0
        updated_rows = 0

        # Create session
        session = create_session_from_str(create_enginestr_from_values(mysql=cfg.mysql))

        for row in reader:
            # Convert empty strings to None
            playerID = row["playerID"] or None
            yearID = row["yearID"] or None
            teamID = row["teamID"] or None
            gameID = row["gameID"] or None
            lgID = row["lgID"] or None
            GP = int(row["GP"]) if row["GP"] else None
            startingPos = int(row["startingPos"]) if row["startingPos"] else None

            # Check if playerID exists in the people table
            player_exists = session.query(People).filter_by(playerID=playerID).first()

            if not player_exists:
                print(
                    f"playerID {playerID} does not exist in the people table. Skipping row."
                )
                continue

            lg_exists = session.query(Leagues).filter_by(lgID=lgID).first()

            if not lg_exists:
                print(f"lgID {lgID} does not exist in the leagues table. Skipping row.")
                continue

            # Check if a row with the same playerID, yearID, teamID, and gameID exists
            existing_entry = (
                session.query(AllstarFull)
                .filter_by(
                    playerID=playerID,
                    yearID=yearID,
                    lgID=lgID,
                    teamID=teamID,
                )
                .first()
            )

            if existing_entry:
                existing_entry.gameID = gameID
                existing_entry.GP = GP
                existing_entry.startingPos = startingPos
                updated_rows += 1
            else:
                # Insert a new record
                new_entry = AllstarFull(
                    playerID=playerID,
                    yearID=yearID,
                    teamID=teamID,
                    gameID=gameID,
                    lgID=lgID,
                    GP=GP,
                    startingPos=startingPos,
                )
                session.add(new_entry)
                new_rows += 1

            session.commit()

    session.close()
    return {"new_rows": new_rows, "updated_rows": updated_rows}
