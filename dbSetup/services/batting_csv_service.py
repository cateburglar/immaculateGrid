import csv

import csi3335f2024 as cfg
from models import Batting, People, Teams
from utils import create_enginestr_from_values, create_session_from_str, get_csv_path

def upload_batting_csv():
    # TODO: Read from Batting.csv AND BattingPost.csv?
    print("updating batting table")
    csv_file_path = get_csv_path("Batting.csv")

    if len(csv_file_path) == 0:
        print("Error: Batting.csv not found")
        return

    # Process CSV
    try:
        print(update_batting_from_csv(csv_file_path))
        print("File processed successfully")
    except Exception as e:
        print(f"Error: {str(e)}")

def update_batting_from_csv(file_path):
    with open(file_path, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        new_rows = 0
        updated_rows = 0
        peopleNotExist=0
        teamNotExists=0
        skipCount=0

        # Create session
        session = create_session_from_str(create_enginestr_from_values(mysql=cfg.mysql))
        for row in reader:
            # TODO: What is G_old in csv?
            # lgID is present in the csv but not in our database
            # lgID=row['lgID'],
            # TODO: G vs B_batting in csv??

            # Add the following 2 lines for debugging
            # print("Row being processed:", row)
            # print("Row keys:", row.keys())
            batting_record = Batting(
                playerID=row['playerID'],
                yearId=int(row['yearID']),
                stint=int(row['stint']),
                teamID=row['teamID'],
                b_G=int(row['G']) if row['G'] else None,
                b_AB=int(row['AB']) if row['AB'] else None,
                b_R=int(row['R']) if row['R'] else None,
                b_H=int(row['H']) if row['H'] else None,
                b_2B=int(row['2B']) if row['2B'] else None,
                b_3B=int(row['3B']) if row['3B'] else None,
                b_HR=int(row['HR']) if row['HR'] else None,
                b_RBI=int(row['RBI']) if row['RBI'] else None,
                b_SB=int(row['SB']) if row['SB'] else None,
                b_CS=int(row['CS']) if row['CS'] else None,
                b_BB=int(row['BB']) if row['BB'] else None,
                b_SO=int(row['SO']) if row['SO'] else None,
                b_IBB=int(row['IBB']) if row['IBB'] else None,
                b_HBP=int(row['HBP']) if row['HBP'] else None,
                b_SH=int(row['SH']) if row['SH'] else None,
                b_SF=int(row['SF']) if row['SF'] else None,
                b_GIDP= int(row['GIDP']) if row['GIDP'] else None
            )

            # Check if playerID exists in the people table
            player_exists = session.query(People).filter_by(playerID=batting_record.playerID).first()

            if not player_exists:
                peopleNotExist+=1
                #if we make an error log, message can go here
                continue

            #check if teamid exists in teams table
            team_exists = session.query(Teams).filter_by(teamID=batting_record.teamID).first()
            
            if not team_exists:
                teamNotExists+=1
                #if we make an error log, a message could go here.
                continue

            # Check if a row with the same playerID, yearID, teamID, and stint exists
            existing_entry = (
                session.query(Batting)
                .filter_by(
                    playerID=batting_record.playerID,
                    yearId=batting_record.yearId,
                    teamID=batting_record.teamID,
                    stint=batting_record.stint,
                )
                .first()
            )

            if existing_entry:
                skipCount+=1
                #if we make error log, message can go here
                continue
            else:
                # Insert a new record
                session.add(batting_record)
                new_rows += 1

            session.commit()
    session.close()
    return {"new_rows": new_rows, "rows skipped bc already existed: ": skipCount,
            "rows skipped bc their playerid didn't exist in people table: ": peopleNotExist, 
            "rows skipped bc their teamid didnt exist in teams table: ": teamNotExists}
