import csv

import csi3335f2024 as cfg
from models import HomeGames, People, Teams #, Parks
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
        peopleNotExist=0
        teamNotExist=0
        skipCount=0

        # Create session
        session = create_session_from_str(create_enginestr_from_values(mysql=cfg.mysql))

        for row in reader:
            homegames_record = HomeGames(
                teamID = row['teamkey']
                parkID = row['parkkey']
                yearID = row['yearkey']
                firstGame = row['spanfirst'] or None
                lastGame = row['spanlast'] or None
                games = row['games'] or None
                openings = row['openings'] or None
                attendance = row['attendance'] or None         
            )

            # Check if park exists in the parks table
           # park_exists = session.query(Parks).filter_by(playerID=homegames_record.parkID).first()

            #if not park_exists:
             #   peopleNotExist+=1
              #  print(
               #     f"playerID {park_exists.playerID} does not exist in the people table. Skipping row."
                #)
                #continue

            #check if teamid exists in teams table
            team_exists = session.query(Teams).filter_by(teamID=homegames_record.teamID).first()
            
            if not team_exists:
                teamNotExist+=1
                #if we make an error log, a message could go here.
                continue

            # Check if a row with the same playerID, yearID, teamID, and stint exists
            existing_entry = (
                session.query(HomeGames)
                .filter_by(
                    yearID=homegames_record.yearID,
                    teamID=homegames_record.teamID,
                    parkID=homegames_record.parkID,
                )
                .first()
            )
            if existing_entry:
                skipCount+=1
                #if we make an error log, message can go here
                continue
            
            else:
                # Insert a new record
                session.add(homegames_record)
                new_rows += 1

            session.commit()

    session.close()
    return {"new_rows": new_rows, "rows skipped bc already exist: ": skipCount,
            "rows skipped bc their playerid didn't exist in people table: ": peopleNotExist, 
            "rows skipped bc their teamid didnt exist in teams table: ": teamNotExist}
