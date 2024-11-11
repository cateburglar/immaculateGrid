import csv

import csi3335f2024 as cfg
from models import Appearances, People
from utils import create_enginestr_from_values, create_session_from_str, get_csv_path


def upload_appearances_csv():
    print("Updating appearances table")
    csv_file_path = get_csv_path("Appearances.csv")

    if len(csv_file_path) == 0:
        print("Error: Appearances.csv not found")
        return

    # Process the CSV file
    try:
        print(update_appearances_from_csv(csv_file_path))
        print("File processed successfully")
    except Exception as e:
        print(f"Error: {str(e)}")


def update_appearances_from_csv(file_path):
    with open(file_path, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        new_rows = 0
        updated_rows = 0

        # Create session
        session = create_session_from_str(create_enginestr_from_values(mysql=cfg.mysql))
        skipCount=0
        peopleNotExist=0
        for row in reader:
            appearances_record = Appearances(
                playerID = row["playerID"],
                yearID = int(row["yearID"]),
                teamID = int(row["teamID"]),
                G_all = row["G_all"] or None,
                GS = row["GS"] or None,
                G_batting = row["G_batting"] or None,
                G_defense = row["G_defense"] or None,
                G_p = row["G_p"] or None,
                G_c = row["G_c"] or None,
                G_1b = row["G_1b"] or None,
                G_2b = row["G_2b"] or None,
                G_3b = row["G_3b"] or None,
                G_ss = row["G_ss"] or None,
                G_lf = row["G_lf"] or None,
                G_cf = row["G_cf"] or None,
                G_rf = row["G_rf"] or None,
                G_of = row["G_of"] or None,
                G_dh = row["G_dh"] or None,
                G_ph = row["G_ph"] or None,
                G_pr = row["G_pr"] or None,
            )

            # Check if playerID exists in the people table
            player_exists = session.query(People).filter_by(playerID=appearances_record.playerID).first()

            if not player_exists:
                peopleNotExist+=1
                print(
                    f"playerID {appearances_record.playerID} does not exist in the people table. Skipping row."
                )
                continue


            # Check if a row with the same playerID, yearID, teamID, and stint exists
            existing_entry = (
                session.query(Appearances)
                .filter_by(
                    playerID=appearances_record.playerID,
                    yearID=appearances_record.yearID,
                    teamID=appearances_record.teamID,
                )
                .first()
            )
            if existing_entry:
                skipCount+=1
                print( f"error- row with matching playerID, yearId, teamid, and stint exists for playerID {appearances_record.playerID}. Skipping row.")
                continue
            else:
                # Insert a new record
                new_entry = Appearances(
                    playerID=appearances_record.playerID,
                    yearID=appearances_record.yearID,
                    teamID=appearances_record.teamID,
                )
                session.add(new_entry)
                new_rows += 1

            session.commit()
        print(f"{skipCount} rows with matching teamids, yearids, and playerids existed. skipped those rows.")
        print(f"{peopleNotExist} people were skipped because they didn't exist in people table")

    session.close()
    return {"new_rows": new_rows, "updated_rows": updated_rows}