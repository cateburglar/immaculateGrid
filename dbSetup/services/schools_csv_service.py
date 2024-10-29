import csv

import csi3335f2024 as cfg
from models import Schools
from utils import create_enginestr_from_values, create_session_from_str, get_csv_path


def upload_schools_csv():
    csv_file_path = get_csv_path("Schools.csv")

    if len(csv_file_path) == 0:
        print("Error: Schools.csv not found")
        return

    # Process the CSV file
    try:
        print(update_teams_from_csv(csv_file_path))
        print("File processed successfully")
    except Exception as e:
        print(f"Error: {str(e)}")


def update_teams_from_csv(file_path):
    with open(file=file_path, newline="") as csvfile:
        reader = csv.reader(csvfile)
        new_rows = 0
        updated_rows = 0

        # Create session
        session = create_session_from_str(create_enginestr_from_values(cfg.mysql))

        # Parse each row
        for row in reader:
            schoolId = row[0] or None
            school_name = row[1] or None
            if len(row) > 5:
                school_city = row[3] or None
                school_state = row[4] or None
                school_country = row[5] or None
            else:
                school_city = row[2] or None
                school_state = row[3] or None
                school_country = row[4] or None

            # Check if team already exists
            existing_entry = (
                session.query(Schools)
                .filter_by(
                    schoolId=schoolId,
                )
                .first()
            )

            if existing_entry:
                existing_entry.school_name = school_name
                existing_entry.school_city = school_city
                existing_entry.school_state = school_state
                existing_entry.school_country = school_country
                updated_rows += 1
            else:
                new_entry = Schools(
                    schoolId=schoolId,
                    school_name=school_name,
                    school_city=school_city,
                    school_state=school_state,
                    school_country=school_country,
                )
                session.add(new_entry)
                new_rows += 1

            session.commit()

    session.close()
    return {"new_rows": new_rows, "updated_rows": updated_rows}
