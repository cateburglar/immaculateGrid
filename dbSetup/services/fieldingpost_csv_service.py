import csv

import csi3335f2024 as cfg
from models import People, Teams, FieldingPost
from utils import create_enginestr_from_values, create_session_from_str, get_csv_path


def upload_fieldingpost_csv():
    print("Updating fieldingpost table")
    csv_file_path = get_csv_path("FieldingPost.csv")

    if len(csv_file_path) == 0:
        print("Error: FieldingPost.csv not found")
        return

    # Process the CSV file
    try:
        print(update_fieldingpost_from_csv(csv_file_path))
        print("File processed successfully")
    except Exception as e:
        print(f"Error: {str(e)}")


def update_fieldingpost_from_csv(file_path):
    with open(file_path, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        new_rows = 0
        peopleNotExist=0
        teamNotExist=0
        skipCount=0

        # Create session
        session = create_session_from_str(create_enginestr_from_values(mysql=cfg.mysql))

        for row in reader:
            fieldingpost_record = FieldingPost(
               playerID=row['playerID'],
                yearID=int(row['yearID']),
                teamID=row['teamID'],
                lgID=row["lgID"] or None,
                round=row["round"] or None,
                position=row["POS"] or None,
                f_G=row['G'],
                f_GS=row['GS'],
                f_InnOuts=row['InnOuts'],
                f_PO=row['PO'],
                f_A=row['A'],
                f_E=row['E'],
                f_DP=row['DP'],
                f_TP=row['TP'],
                f_PB=row['PB']
            )

            # Check if playerID exists in the people table
            player_exists = session.query(People).filter_by(playerID=fieldingpost_record.playerID).first()

            if not player_exists:
                peopleNotExist+=1
                #if we make an error log, message could go here.
                continue

            #check if teamid exists in teams table
            team_exists = session.query(Teams).filter_by(teamID=fieldingpost_record.teamID).first()
            
            if not team_exists:
                teamNotExist+=1
                #if we make an error log, a message could go here.
                continue

            # Check if a row with the same playerID, yearID, teamID, and stint exists
            existing_entry = (
                session.query(FieldingPost)
                .filter_by(
                    playerID=fieldingpost_record.playerID,
                    yearID=fieldingpost_record.yearID,
                    teamID=fieldingpost_record.teamID,
                )
                .first()
            )
            if existing_entry:
                skipCount+=1
                #if we make an error log, message can go here
                continue
            
            else:
                # Insert a new record
                session.add(fieldingpost_record)
                new_rows += 1

            session.commit()

    session.close()
    return {"new_rows": new_rows, "rows skipped bc already exist: ": skipCount,
            "rows skipped bc their playerid didn't exist in people table: ": peopleNotExist, 
            "rows skipped bc their teamid didnt exist in teams table: ": teamNotExist}
