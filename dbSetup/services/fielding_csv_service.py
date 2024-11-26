import csv

import csi3335f2024 as cfg
from models import Fielding, People, Teams
from utils import create_enginestr_from_values, create_session_from_str, get_csv_path


def upload_fielding_csv():
    print("Updating fielding table")
    csv_file_path = get_csv_path("Fielding.csv")

    if len(csv_file_path) == 0:
        print("Error: Fielding.csv not found")
        return

    # Process the CSV file
    try:
        print(update_fielding_from_csv(csv_file_path))
        print("File processed successfully")
    except Exception as e:
        print(f"Error: {str(e)}")


def update_fielding_from_csv(file_path):
    with open(file_path, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        new_rows = 0
        peopleNotExist=0
        teamNotExist=0
        skipCount=0

        # Create session
        session = create_session_from_str(create_enginestr_from_values(mysql=cfg.mysql))

        for row in reader:
            fielding_record = Fielding(
                playerID=row['playerID'],
                yearID=int(row['yearID']),
                teamID=row['teamID'],
                stint=int(row['stint']),
                position=row['POS'] if row['POS'] else None,
                f_G=int(row['G']) if row['G'] else None,
                f_GS=int(row['GS']) if row['GS'] else None,
                f_InnOuts=int(row['InnOuts']) if row['InnOuts'] else None,
                f_PO=int(row['PO']) if row['PO'] else None,
                f_A=int(row['A']) if row['A'] else None,
                f_E=int(row['E']) if row['E'] else None,
                f_DP=int(row['DP']) if row['DP'] else None,
                f_PB=int(row['PB']) if row['PB'] else None,
                f_WP=int(row['WP']) if row['WP'] else None,
                f_SB=int(row['SB']) if row['SB'] else None,
                f_CS=int(row['CS']) if row['CS'] else None,
                f_ZR=float(row['ZR']) if row['ZR'] else None,
            )

            # Check if playerID exists in the people table
            player_exists = session.query(People).filter_by(playerID=fielding_record.playerID).first()

            if not player_exists:
                peopleNotExist+=1
                #if we make an error log, message could go here.
                continue

            #check if teamid exists in teams table
            team_exists = session.query(Teams).filter_by(teamID=fielding_record.teamID).first()
            
            if not team_exists:
                teamNotExist+=1
                #if we make an error log, a message could go here.
                continue

            # Check if a row with the same playerID, yearID, teamID, and stint exists
            existing_entry = (
                session.query(Fielding)
                .filter_by(
                    playerID=fielding_record.playerID,
                    yearID=fielding_record.yearID,
                    teamID=fielding_record.teamID,
                    stint=fielding_record.stint,
                )
                .first()
            )
            if existing_entry:
                skipCount+=1
                #if we make an error log, message can go here
                continue
            
            else:
                # Insert a new record
                session.add(fielding_record)
                new_rows += 1

            session.commit()

    session.close()
    return {"new_rows": new_rows, "rows skipped bc already exist: ": skipCount,
            "rows skipped bc their playerid didn't exist in people table: ": peopleNotExist, 
            "rows skipped bc their teamid didnt exist in teams table: ": teamNotExist}
