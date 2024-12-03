import csv

import csi3335f2024 as cfg
from models import Pitching, People, Teams
from utils import create_enginestr_from_values, create_session_from_str, get_csv_path


def upload_pitching_csv():
    print("Updating pitching table")
    csv_file_path = get_csv_path("Pitching.csv")

    if len(csv_file_path) == 0:
        print("Error: Pitching.csv not found")
        return

    # Process the CSV file
    try:
        print(update_pitching_from_csv(csv_file_path))
        print("File processed successfully")
    except Exception as e:
        print(f"Error: {str(e)}")


def update_pitching_from_csv(file_path):
    with open(file_path, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        new_rows = 0
        teamNotExists=0
        updateCount=0
        peopleNotExist=0
        batch_counter, batch_size = 0,500

        # Create session
        session = create_session_from_str(create_enginestr_from_values(mysql=cfg.mysql))
        for row in reader:
            pitching_record = Pitching(
                playerID=row['playerID'],
                yearID=int(row['yearID']),
                teamID=row['teamID'],
                stint=int(row['stint']),
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
                p_HR=int(row['HR']) if row['HR'] else None,
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
            player_exists = session.query(People).filter_by(playerID=pitching_record.playerID).first()

            if not player_exists:
                peopleNotExist+=1
                #if we make an error log, message can go here
                continue

            #check if teamid exists in teams table
            team_exists = session.query(Teams).filter_by(teamID=pitching_record.teamID).first()

            if not team_exists:
                teamNotExists+=1
                #if we make an error log, a message could go here.
                continue

            # Check if a row with the same playerID, yearID, teamID, and stint exists
            existing_entry = (
                session.query(Pitching)
                .filter_by(
                    playerID=pitching_record.playerID,
                    yearID=pitching_record.yearID,
                    teamID=pitching_record.teamID,
                    stint=pitching_record.stint,
                )
                .first()
            )

            # Check for existing record
            if existing_entry:
                for column in Pitching.__table__.columns:
                    # Skip the 'ID' column as it should not be modified
                    if column.name == 'pitching_ID':
                        continue

                    updated = False
                    new_value = getattr(pitching_record, column.name)
                    existing_value = getattr(existing_entry, column.name)

                    #skip if both columns are null
                    if new_value is None and existing_value is None:
                        continue

                    # If the values are different, update the existing record
                    if existing_value is None or new_value != existing_value :
                        setattr(existing_entry, column.name, new_value)
                        updated = True

                if updated:
                    updateCount += 1  # Only count as updated if something changed
            else:
                new_rows += 1
                session.add(pitching_record)

            batch_counter += 1

            # Commit in batches
            if batch_counter >= batch_size:
                session.commit()
                batch_counter = 0

        # Commit remaining batch
        session.commit()
        session.close()
    return {"new_rows": new_rows, "rows updated: ": updateCount,
            "rows skipped bc their playerid didn't exist in people table: ": peopleNotExist,
            "rows skipped bc their teamid didnt exist in teams table: ": teamNotExists}
