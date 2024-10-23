import csv

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import app.csi3335f2024 as cfg
from app.models import AllstarFull


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
            + ":3306/"
            + cfg.mysql["db"]
        )
        engine = create_engine(enginestr)

        # Create session
        Session = sessionmaker(bind=engine)
        session = Session()

        for row in reader:
            # Check if a row with the same playerID, yearID, teamID, and gameID exists
            existing_entry = (
                session.query(AllstarFull)
                .filter_by(
                    playerID=row["playerID"],
                    yearID=row["yearID"],
                    teamID=row["teamID"],
                    gameID=row["gameID"],
                )
                .first()
            )

            if existing_entry:
                # Update the existing record
                existing_entry.lgID = row["lgID"]
                existing_entry.GP = row.get("GP", None)  # Use None for missing data
                existing_entry.startingPos = row.get("startingPos", None)
                updated_rows += 1
            else:
                # Insert a new record if no match found
                new_entry = AllstarFull(
                    playerID=row["playerID"],
                    yearID=row["yearID"],
                    teamID=row["teamID"],
                    lgID=row["lgID"],
                    gameID=row.get("gameID"),  # Nullable field
                    GP=row.get("GP", None),
                    startingPos=row.get("startingPos", None),
                )
                session.add(new_entry)
                new_rows += 1

        # Commit the session to apply updates and inserts
        session.commit()

        print(f"{updated_rows} rows updated, {new_rows} new rows added.")
