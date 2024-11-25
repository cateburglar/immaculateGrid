import csv

import csi3335f2024 as cfg
from models import PitchingPost, People, Teams
from utils import create_enginestr_from_values, create_session_from_str, get_csv_path


def upload_pitchingpost_csv():
    print("Updating pitching post table")
    csv_file_path = get_csv_path("PitchingPost.csv")

    if len(csv_file_path) == 0:
        print("Error: PitchingPost.csv not found")
        return

    # Process the CSV file
    try:
        print(update_pitchingpost_from_csv(csv_file_path))
        print("File processed successfully")
    except Exception as e:
        print(f"Error: {str(e)}")


def update_pitchingpost_from_csv(file_path):
    with open(file_path, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        new_rows = 0
        peopleNotExist=0
        teamNotExists=0
        skipCount=0

        # Create session
        session = create_session_from_str(create_enginestr_from_values(mysql=cfg.mysql))
        skipCount=0
        peopleNotExist=0
        for row in reader:
            pitchingpost_record = PitchingPost(
                playerID=row['playerID'],
                yearID=int(row['yearID']),
                teamID=row['teamID'],
                round=row['round'],
                p_W=int(row['W']) if row['W'] else None,
                p_L=int(row['L']) if row['L'] else None,
                p_G=int(row['G']) if row['G'] else None,
                p_GS=int(row['GS']) if row['GS'] else None,
                p_CG=int(row['CG']) if row['CG'] else None,
                p_SHO=int(row['SHO']) if row['SHO'] else None,
                p_SV=int(row['SV']) if row['SV'] else None,
                p_IPouts=int(row['IPouts']) if row['IPouts'] else None,
                p_H=int(row['H']) if row['H'] else None,
                p_ER=int(row['ER']) if row['ER'] else None,
                p_BB=int(row['BB']) if row['BB'] else None,
                p_SO=int(row['SO']) if row['SO'] else None,
                p_BAOpp=float(row['BAOpp']) if row['BAOpp'] else None,
                p_ERA=float(row['ERA']) if row['ERA'] else None,
                p_IBB=int(row['IBB']) if row['IBB'] else None,
                p_WP=int(row['WP']) if row['WP'] else None,
                p_HBP=int(row['HBP']) if row['HBP'] else None,
                p_BK=int(row['BK']) if row['BK'] else None,
                p_BFP=int(row['BFP']) if row['BFP'] else None,
                p_GF=int(row['GF']) if row['GF'] else None,
                p_R=int(row['R']) if row['R'] else None,
                p_SH=int(row['SH']) if row['SH'] else None,
                p_SF=int(row['SF']) if row['SF'] else None,
                p_GIDP=int(row['GIDP']) if row['GIDP'] else None
            )

            # Check if playerID exists in the people table
            player_exists = session.query(People).filter_by(playerID=pitchingpost_record.playerID).first()

            if not player_exists:
                peopleNotExist+=1
                #if we make an error log, message can go here
                continue

            #check if teamid exists in teams table
            team_exists = session.query(Teams).filter_by(teamID=pitchingpost_record.teamID).first()
            
            if not team_exists:
                teamNotExists+=1
                #if we make an error log, a message could go here.
                continue

            # Check if a row with the same playerID, yearID, teamID, and round exists
            existing_entry = (
                session.query(PitchingPost)
                .filter_by(
                    playerID=pitchingpost_record.playerID,
                    yearID=pitchingpost_record.yearID,
                    teamID=pitchingpost_record.teamID,
                    round=pitchingpost_record.round,
                )
                .first()
            )

            if existing_entry:
                skipCount+=1
                #if we make error log, message can go here
                continue
            else:
                # Insert a new record
                session.add(pitchingpost_record)
                new_rows += 1

            session.commit()
    session.close()
    return {"new_rows": new_rows, "rows skipped bc already existed: ": skipCount,
            "rows skipped bc their playerid didn't exist in people table: ": peopleNotExist, 
            "rows skipped bc their teamid didnt exist in teams table: ": teamNotExists}
