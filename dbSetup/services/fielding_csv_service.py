import csv

import csi3335f2024 as cfg
from models import Fielding, People
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
        updated_rows = 0

        # Create session
        session = create_session_from_str(create_enginestr_from_values(mysql=cfg.mysql))

        for row in reader:
            fielding_record = Fielding(
                playerID=row['playerID'],
                yearID=int(row['yearID']),
                teamID=row['teamID'],
                stint=int(row['stint']),
                position=row['position'],
                f_G=row['G'],
                f_GS=row['GS'],
                f_InnOuts=row['InnOuts'],
                f_PO=row['PO'],
                f_A=row['A'],
                f_E=row['E'],
                f_DP=row['DP'],
                f_PB=row['PB'],
                f_WP=row['WP'],
                f_SB=row['SB'],
                f_CS=row['CS'],
                f_ZR=row['ZR'],
            )

            # Check if playerID exists in the people table
            player_exists = session.query(Fielding).filter_by(playerID=fielding_record.playerID).first()

            if not player_exists:
                print(
                    f"playerID {fielding_record.playerID} does not exist in the people table. Skipping row."
                )
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
                print(
                    f"error- playerID {fielding_record.playerID} already exists. Skipping row."
                )
                continue
            else:
                # Insert a new record
                new_entry = Fielding(
                    playerID=fielding_record.playerID,
                    yearID=fielding_record.yearID,
                    teamID=fielding_record.teamID,
                    stint = fielding_record.stint,
                )
                session.add(new_entry)
                new_rows += 1

            session.commit()

    session.close()
    return {"new_rows": new_rows, "updated_rows": updated_rows}
