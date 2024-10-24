import csv
import os

import csi3335f2024 as cfg
from models import AllstarFull, Leagues, People
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def model_to_dict(model):
    """
    Convert a SQLAlchemy model instance to a dictionary.
    """
    return {
        column.name: getattr(model, column.name) for column in model.__table__.columns
    }


def upload_allstarfull_csv():
    # Define the path to the CSV file
    base_dir = os.path.abspath(os.path.dirname(__file__))
    csv_file_path = os.path.join(base_dir, "..", "static", "csv", "AllstarFull.csv")

    # Check if the file exists
    if not os.path.exists(csv_file_path):
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

        # Create engine
        enginestr = (
            "mysql+pymysql://"
            + cfg.mysql["user"]
            + ":"
            + cfg.mysql["password"]
            + "@"
            + cfg.mysql["host"]
            + "/"
            + cfg.mysql["db"]
        )
        engine = create_engine(enginestr)
        Session = sessionmaker(bind=engine)
        session = Session()

        for row in reader:
            # Convert empty strings to None
            playerID = row["playerID"] or None
            yearID = row["yearID"] or None
            teamID = row["teamID"] or None
            gameID = row["gameID"] or None
            lgID = row["lgID"] or None
            GP = int(row["GP"]) if row["GP"] else None
            startingPos = int(row["startingPos"]) if row["startingPos"] else None

            # Debug prints
            print(
                f"Processing row: playerID={playerID}, yearID={yearID}, teamID={teamID}, gameID={gameID}, lgID={lgID}, GP={GP}, startingPos={startingPos}"
            )

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
                # Update the existing record
                existing_entry.lgID = lgID
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
