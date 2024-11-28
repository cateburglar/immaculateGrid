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
        updated_rows =0

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

            existing_entry = (
                session.query(Parks)
                .filter_by(
                    parkID=parks_record.parkID
                )
                .first()
            )

            # Check for existing record
            if existing_entry:
                for column in Parks.__table__.columns:
                    # Skip the 'ID' column as it should not be modified
                    if column.name == 'parkID':
                        continue

                    updated = False
                    new_value = getattr(parks_record, column.name)
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
                session.add(parks_record)
            
        #commit remaining batch
        session.commit()
        session.close()

    return {"new rows": new_rows, "updated rows": updated_rows}
