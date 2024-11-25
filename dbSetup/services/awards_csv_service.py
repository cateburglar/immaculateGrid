import csv

import csi3335f2024 as cfg
from models import Awards, People, Teams
from utils import create_enginestr_from_values, create_session_from_str, get_csv_path


def upload_awards_csv():
    print("Updating awards table")
    awards_players_file_path = get_csv_path("AwardsPlayers.csv")
    awards_managers_file_path = get_csv_path("AwardsManagers.csv")
    
    if len(awards_players_file_path) == 0 or len(awards_managers_file_path) == 0:
        print("Error: One or both award CSV files not found")
        return

    # Process the Awards CSV files
    try:
        print(update_awards_from_csv(awards_players_file_path, 'player'))
        print(update_awards_from_csv(awards_managers_file_path, 'manager'))
        print("Awards files processed successfully")
    except Exception as e:
        print(f"Error: {str(e)}")


def update_awards_from_csv(file_path, award_type):
    with open(file_path, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        new_rows = 0
        peopleNotExist = 0
        skipCount = 0

        # Create session
        session = create_session_from_str(create_enginestr_from_values(mysql=cfg.mysql))
        
        for row in reader:
            awards_record = Awards(
                playerID=row['playerID'],
                awardID=row['awardID'],
                yearID=int(row['yearID']),
                lgID=row['lgID'],
                tie=row.get('tie'),
                notes=row.get('notes')
            )

            # Check if playerID exists in the people table
            player_exists = session.query(People).filter_by(playerID=awards_record.playerID).first()

            if not player_exists:
                peopleNotExist += 1
                continue

            # Check if a row with the same playerID, awardID, and yearID exists
            existing_entry = (
                session.query(Awards)
                .filter_by(
                    playerID=awards_record.playerID,
                    awardID=awards_record.awardID,
                    yearID=awards_record.yearID
                )
                .first()
            )

            if existing_entry:
                skipCount += 1
                continue
            else:
                # Insert a new record
                session.add(awards_record)
                new_rows += 1

        session.commit()
        session.close()
        return {
            "new_rows": new_rows, 
            "rows skipped bc already existed": skipCount,
            "rows skipped bc their playerID didn't exist in people table": peopleNotExist
        }

