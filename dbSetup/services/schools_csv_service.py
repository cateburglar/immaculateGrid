import csv

from csi3335f2024 import mysql
from models import Schools
from sqlalchemy.exc import SQLAlchemyError
from utils import create_enginestr_from_values, create_session_from_str, get_csv_path


def upload_schools_csv():
    print("Updating schools table")
    csv_file_path = get_csv_path("Schools.csv")

    if len(csv_file_path) == 0:
        raise FileNotFoundError("Error: Schools.csv not found")

    # Process the CSV file
    try:
        result = update_schools_from_csv(csv_file_path)
        print(f"File processed successfully: {result}")
    except Exception as e:
        raise RuntimeError(f"Error processing file: {str(e)}")


def update_schools_from_csv(file_path):
    try:
        with open(file_path, newline="") as csvfile:
            reader = csv.reader(csvfile)
            session = create_session_from_str(create_enginestr_from_values(mysql))
            counts = {"updated_rows": 0}
            # Process rows
            for row in reader:
                process_row(row, session, counts)
            # Commit updates
            session.commit()
    except (csv.Error, SQLAlchemyError) as e:
        session.rollback()
        raise RuntimeError(f"Error updating schools from CSV: {str(e)}")
    except Exception as e:
        raise RuntimeError(f"Unexpected error: {str(e)}")

    return counts


def process_row(row, session, counts):
    try:
        # Get the attributes
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

        entry = Schools(
            schoolId=schoolId,
            school_name=school_name,
            school_city=school_city,
            school_state=school_state,
            school_country=school_country,
        )

        session.merge(entry)  # Upsert row
        counts["updated_rows"] += 1  # Update count

    except SQLAlchemyError as e:
        raise RuntimeError(f"Error processing row: {str(e)}")
