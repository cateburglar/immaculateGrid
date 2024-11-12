import csv

import csi3335f2024 as cfg
from models import Parks
from utils import create_enginestr_from_values, create_session_from_str, get_csv_path


def upload_parks_csv():
    print("Updating parks table")
    csv_file_path = get_csv_path("Parks.csv")

    if len(csv_file_path) == 0:
        print("Error: Parks.csv not found")
        return

    # Process the CSV file
    try:
        print(update_parks_from_csv(csv_file_path))
        print("File processed successfully")
    except Exception as e:
        print(f"Error: {str(e)}")


def update_parks_from_csv(file_path):
    with open(file_path, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        new_rows = 0
        skipCount=0

        # Create session
        session = create_session_from_str(create_enginestr_from_values(mysql=cfg.mysql))

        for row in reader:
            parks_record = Parks(
                parkID = row['parkkey'],
                park_alias = row['parkalias'] or None,
                park_name = row['parkname'] or None,
                city = row['city'] or None,
                state = row['state'] or None,
                country = row['country'] or None, 
            )

            # Check if a row with the same playerID, yearID, teamID, and stint exists
            existing_entry = (
                session.query(Parks)
                .filter_by(
                    parkID=parks_record.parkID,
                )
                .first()
            )
            if existing_entry:
                skipCount+=1
                #if we make an error log, message can go here
                continue
            
            else:
                # Insert a new record
                session.add(parks_record)
                new_rows += 1

            session.commit()

    session.close()
    return {"new_rows": new_rows, "rows skipped bc already exist: ": skipCount}
