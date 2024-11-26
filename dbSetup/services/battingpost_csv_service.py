import csv

import csi3335f2024 as cfg
from models import BattingPost, People, Teams
from utils import create_enginestr_from_values, create_session_from_str, get_csv_path

def upload_battingpost_csv():
    print("updating batting post table")
    csv_file_path = get_csv_path("BattingPost.csv")

    if len(csv_file_path) == 0:
        print("Error: BattingPost.csv not found")
        return

    # Process CSV
    try:
        print(update_battingpost_from_csv(csv_file_path))
        print("File processed successfully")
    except Exception as e:
        print(f"Error: {str(e)}")

def update_battingpost_from_csv(file_path):
    with open(file_path, newline="") as csvfile:
        # Create session
        session = create_session_from_str(create_enginestr_from_values(mysql=cfg.mysql))

        reader = csv.DictReader(csvfile)
        inserted_rows = 0
        updated_rows = 0
        peopleNotExist = 0
        teamNotExists = 0
        batch_size = 500  # Commit in batches
        batch_counter = 0

        for row in reader:
            # Create or update the batting post record
            battingpost_record = BattingPost(
                playerID=row['playerID'],
                yearId=int(row['yearID']),
                teamID=row['teamID'],
                round=row['round'],
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
                b_GIDP=int(row['GIDP']) if row['GIDP'] else None,
            )

            # Check if playerID exists in people table
            player_exists = session.query(People).filter_by(playerID=battingpost_record.playerID).first()
            if not player_exists:
                peopleNotExist+=1
                #if we make an error log, a message can go here
                continue

            # Check if teamid exists in teams table
            team_exists = session.query(Teams).filter_by(teamID=battingpost_record.teamID).first()
            if not team_exists:
                teamNotExists+=1
                #if we make an error log, a message can go here
                continue

            existing_entry = (
                session.query(BattingPost)
                .filter_by(
                    playerID=battingpost_record.playerID,
                    yearId=battingpost_record.yearId,
                    teamID=battingpost_record.teamID,
                    round=battingpost_record.round,
                )
                .first()
            )

            # Determine if it's an insert or update
            if existing_entry:
                updated_rows += 1
            else:
                inserted_rows += 1

            # Use merge to handle upsert
            session.merge(battingpost_record)
            batch_counter += 1

            # Commit in batches
            if batch_counter >= batch_size:
                session.commit()
                batch_counter = 0

        # Final commit for remaining records
        session.commit()
        session.close()

    return {
        "inserted_rows": inserted_rows,
        "updated_rows": updated_rows,
        "rows skipped bc their playerID didn't exist in People table": peopleNotExist,
        "rows skipped bc their teamID didn't exist in Teams table": teamNotExists,
    }

