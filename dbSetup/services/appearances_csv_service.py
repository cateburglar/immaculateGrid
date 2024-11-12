import csv

import csi3335f2024 as cfg
from models import Appearances, People, Teams
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
        peopleNotExist=0
        teamNotExists=0
        skipCount=0

        # Create session
        session = create_session_from_str(create_enginestr_from_values(mysql=cfg.mysql))

        #read in all csv data lol
        for row in reader:
            appearances_record = Appearances(
                playerID = row["playerID"],
                yearID = int(row["yearID"]),
                teamID = row["teamID"],
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
                #if we make an error log, message can go here
                continue
            
            #check if teamid exists in teams table
            team_exists = session.query(Teams).filter_by(teamID=appearances_record.teamID).first()
            
            if not team_exists:
                teamNotExists+=1
                #if we make an error log, a message could go here.
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

            #dont update any currently existing rows, just skip it
            if existing_entry:
                skipCount+=1
                #if we make an error log, a message could go here.
                continue
            else:
                # Insert a new record
                session.add(appearances_record)
                new_rows += 1

            session.commit()

    session.close()
    return {"new_rows": new_rows, "rows skipped bc already exist: ": skipCount,
            "rows skipped bc their playerid didn't exist in people table: ": peopleNotExist, 
            "rows skipped bc their teamid didnt exist in teams table: ": teamNotExists}