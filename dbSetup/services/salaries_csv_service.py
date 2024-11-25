import csv

import csi3335f2024 as cfg
from models import People, Teams, Salaries
from utils import create_enginestr_from_values, create_session_from_str, get_csv_path


def upload_salaries_csv():
    print("Updating salaries table")
    csv_file_path = get_csv_path("Salaries.csv")

    if len(csv_file_path) == 0:
        print("Error: Pitching.csv not found")
        return

    # Process the CSV file
    try:
        print(update_salaries_from_csv(csv_file_path))
        print("File processed successfully")
    except Exception as e:
        print(f"Error: {str(e)}")

def update_salaries_from_csv(file_path):
    with open(file_path, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        new_rows = 0
        peopleNotExist=0
        teamNotExist=0
        skipCount=0

        # Create session
        session = create_session_from_str(create_enginestr_from_values(mysql=cfg.mysql))

        for row in reader:
            salaries_record = Salaries(
                playerID=row['playerID'],
                yearID=int(row['yearID']),
                teamID=row['teamID'],
                salary=float(row['salary']),
            )

            # Check if playerID exists in the people table
            player_exists = session.query(People).filter_by(playerID=salaries_record.playerID).first()

            if not player_exists:
                peopleNotExist+=1
                #if we make an error log, message could go here.
                continue

            #check if teamid exists in teams table
            team_exists = session.query(Teams).filter_by(teamID=salaries_record.teamID).first()
            
            if not team_exists:
                teamNotExist+=1
                #if we make an error log, a message could go here.
                continue

            # Check if a row with the same playerID, yearID, and teamID exists
            existing_entry = (
                session.query(Salaries)
                .filter_by(
                    playerID=salaries_record.playerID,
                    yearID=salaries_record.yearID,
                    teamID=salaries_record.teamID,
                )
                .first()
            )
            if existing_entry:
                skipCount+=1
                #if we make an error log, message can go here
                continue
            
            else:
                # Insert a new record
                session.add(salaries_record)
                new_rows += 1

            session.commit()

    session.close()
    return {"new_rows": new_rows, "rows skipped bc already exist: ": skipCount,
            "rows skipped bc their playerid didn't exist in people table: ": peopleNotExist, 
            "rows skipped bc their teamid didnt exist in teams table: ": teamNotExist}


