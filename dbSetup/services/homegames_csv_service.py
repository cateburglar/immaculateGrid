import csv

import csi3335f2024 as cfg
from models import HomeGames, Teams, Parks
from utils import create_enginestr_from_values, create_session_from_str, get_csv_path


def upload_homegames_csv():
    print("Updating homegames table")
    csv_file_path = get_csv_path("HomeGames.csv")

    if len(csv_file_path) == 0:
        print("Error: HomeGames.csv not found")
        return

    # Process the CSV file
    try:
        print(update_homegames_from_csv(csv_file_path))
        print("File processed successfully")
    except Exception as e:
        print(f"Error: {str(e)}")


def update_homegames_from_csv(file_path):
    with open(file_path, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        new_rows = 0
        parksNotExist=0
        teamNotExist=0
        updated_rows=0
        # Create session
        session = create_session_from_str(create_enginestr_from_values(mysql=cfg.mysql))

        for row in reader:
            homegames_record = HomeGames(
                teamID = row['teamkey'],
                parkID = row['parkkey'],
                yearID = row['yearkey'],
                firstGame = row['spanfirst'] or None,
                lastGame = row['spanlast'] or None,
                games = row['games'] or None,
                openings = row['openings'] or None,
                attendance = row['attendance'] or None,     
            )

            # Check if park exists in the parks table
            park_exists = session.query(Parks).filter_by(parkID=homegames_record.parkID).first()

            if not park_exists:
                parksNotExist+=1
                print(
                    f"parkID {homegames_record.parkID} does not exist in the parks table. Skipping row."
                )
                continue

            #check if teamid exists in teams table
            team_exists = session.query(Teams).filter_by(teamID=homegames_record.teamID).first()
            
            if not team_exists:
                teamNotExist+=1
                #if we make an error log, a message could go here.
                continue


            existing_entry = (
                session.query(HomeGames)
                .filter_by(
                    teamID=homegames_record.teamID,
                    yearID=homegames_record.yearID,
                    parkID=homegames_record.parkID,
                )
                .first()
            )

            # Check for existing record
            if existing_entry:
                for column in HomeGames.__table__.columns:
                    # Skip the 'ID' column as it should not be modified
                    if column.name == 'homegames_ID':
                        continue

                    updated = False
                    new_value = getattr(homegames_record, column.name)
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
                session.add(homegames_record)
            
        #commit remaining batch
        session.commit()
        session.close()

    return {"updated rows": new_rows,
            "rows skipped bc their parkid didn't exist in parks table: ": parksNotExist, 
            "rows skipped bc their teamid didnt exist in teams table: ": teamNotExist}
