import csv

import csi3335f2024 as cfg
from models import Leagues, SeriesPost
from utils import create_enginestr_from_values, create_session_from_str, get_csv_path


def upload_seriespost_csv():
    print("Updating seriespost table")
    csv_file_path = get_csv_path("SeriesPost.csv")

    if len(csv_file_path) == 0:
        print("Error: SeriesPost.csv not found")
        return

    # Process the CSV file
    try:
        print(update_seriespost_from_csv(csv_file_path))
        print("File processed successfully")
    except Exception as e:
        print(f"Error: {str(e)}")


def update_seriespost_from_csv(file_path):
    with open(file_path, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        new_rows = 0
        updated_rows = 0

        # Create session
        session = create_session_from_str(create_enginestr_from_values(mysql=cfg.mysql))

        for row in reader:
            teamIDwinner = row["teamIDwinner"] or None
            lgIDwinner = row["lgIDwinner"] or None
            teamIDloser = row["teamIDloser"] or None
            lgIDloser = row["lgIDloser"] or None
            yearID = int(row["yearID"]) if row["yearID"] else None
            round = int(row["round"]) if row["round"] else None
            wins = int(row["wins"]) if row["wins"] else None
            losses = int(row["losses"]) if row["losees"] else None
            ties = int(row["ties"]) if row["ties"] else None

            lg_winner_exists = session.query(Leagues).filter_by(lgID=lgIDwinner).first()

            if not lg_winner_exists:
                print(
                    f"lgIDwinner {lgIDwinner} does not exist in the leagues table. Skipping row."
                )
                continue

            lg_loser_exists = session.query(Leagues).filter_by(lgID=lgIDloser).first()

            if not lg_loser_exists:
                print(
                    f"lgIDloser {lgIDloser} does not exist in the leagues table. Skipping row."
                )
                continue

            # Check if a row with the same playerID, yearID, teamID, and gameID exists
            existing_entry = (
                session.query(SeriesPost)
                .filter_by(
                    teamIDwinner=teamIDwinner,
                    teamIDloser=teamIDloser,
                    yearID=yearID,
                    round=round,
                )
                .first()
            )

            if existing_entry:
                existing_entry.lgIDwinner = lgIDwinner
                existing_entry.lgIDloser = lgIDloser
                existing_entry.wins = wins
                existing_entry.losses = losses
                existing_entry.ties = ties
                updated_rows += 1
            else:
                # Insert a new record
                new_entry = SeriesPost(
                    teamIDwinner=teamIDwinner,
                    lgIDwinner=lgIDwinner,
                    teamIDloser=teamIDwinner,
                    lgIDloser=lgIDloser,
                    yearID=yearID,
                    round=round,
                    wins=wins,
                    losses=losses,
                    ties=ties,
                )
                session.add(new_entry)
                new_rows += 1

            session.commit()

    session.close()
    return {"new_rows": new_rows, "updated_rows": updated_rows}
