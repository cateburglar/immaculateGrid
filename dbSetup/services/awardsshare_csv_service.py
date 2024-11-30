import csv

import csi3335f2024 as cfg
from models import AwardsShare, People
from utils import create_enginestr_from_values, create_session_from_str, get_csv_path

def upload_awardsshare_csv():
    print("Updating awards share table")
    awards_share_players_file_path = get_csv_path("AwardsSharePlayers.csv")
    awards_share_managers_file_path = get_csv_path("AwardsShareManagers.csv")
    
    if len(awards_share_players_file_path) == 0 or len(awards_share_managers_file_path) == 0:
        print("Error: One or both awardsshare CSV files not found")
        return

    # Process the AwardsShare CSV files
    try:
        print("Reading from AwardsSharePlayers.csv")
        print(update_awardsshare_from_csv(awards_share_players_file_path))
        print("Awards share files processed successfully")

        print("Reading from AwardsShareManagers.csv")
        print(update_awardsshare_from_csv(awards_share_managers_file_path))
        print("Awards share files processed successfully")
    except Exception as e:
        print(f"Error: {str(e)}")


def update_awardsshare_from_csv(file_path):
    with open(file_path, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        new_rows = 0
        updated_rows = 0
        peopleNotExist = 0

        # Create session
        session = create_session_from_str(create_enginestr_from_values(mysql=cfg.mysql))

        for row in reader:
            awardsshare_record = AwardsShare(
                awardID=row['awardID'],
                yearID=int(row['yearID']),
                lgID=row['lgID'],
                playerID=row['playerID'],
                pointsWon=float(row['pointsWon']) if row['pointsWon'] else None,
                pointsMax=int(row['pointsMax']) if row['pointsMax'] else None,
                votesFirst=float(row['votesFirst']) if row['votesFirst'] else None
            )

            # Check if playerID exists in the people table
            player_exists = session.query(People).filter_by(playerID=awardsshare_record.playerID).first()

            if not player_exists:
                peopleNotExist += 1
                continue

            # Check if a row with the same playerID, awardID, and yearID exists
            existing_entry = (
                session.query(AwardsShare)
                .filter_by(
                    playerID=awardsshare_record.playerID,
                    awardID=awardsshare_record.awardID,
                    yearID=awardsshare_record.yearID
                )
                .first()
            )

            # Check for existing record
            if existing_entry:
                for column in AwardsShare.__table__.columns:
                    # Skip the 'ID' column as it should not be modified
                    if column.name == 'awardsshare_ID':
                        continue

                    updated = False
                    new_value = getattr(awardsshare_record, column.name)
                    existing_value = getattr(existing_entry, column.name)

                    #skip if both columns are null
                    if new_value is None and existing_value is None:
                        continue

                    # If the values are different, update the existing record
                    if existing_value is None or new_value != existing_value :
                        setattr(existing_entry, column.name, new_value)
                        updated = True

                if updated:
                    updated_rows += 1  # Only count as updated if something changed
            else:
                new_rows += 1
                session.add(awardsshare_record)

        session.commit()
        session.close()
        return {
            "new rows": new_rows, 
            "updated rows": updated_rows,
            "rows skipped bc their playerID didn't exist in people table": peopleNotExist
        }
