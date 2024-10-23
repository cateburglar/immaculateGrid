import csv
import os

from flask import jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import dbSetup.csi3335f2024 as cfg
from dbSetup.models import AllstarFull, Leagues, People


def upload_allstarfull_csv():
    # Define the path to the CSV file
    base_dir = os.path.abspath(os.path.dirname(__file__))
    csv_file_path = os.path.join(base_dir, "..", "static", "csv", "AllstarFull.csv")

    # Check if the file exists
    if not os.path.exists(csv_file_path):
        return jsonify({"error": "Allstarfull.csv not found"}), 404

    # Process the CSV file
    try:
        update_allstarfull_from_csv(csv_file_path)
        return jsonify({"message": "File processed successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


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
            GP = row.get("GP", None)
            startingPos = row.get("startingPos", None)

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
                    teamID=teamID,
                    gameID=gameID,
                    startingPos=startingPos,
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
