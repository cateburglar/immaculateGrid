import csv

from csi3335f2024 import mysql
from models import People
from sqlalchemy.exc import OperationalError
from utils import create_enginestr_from_values, create_session_from_str, get_csv_path


def upload_people_csv():
    print("Updating people table")
    csv_file_path = get_csv_path("People.csv")

    if len(csv_file_path) == 0:
        raise FileNotFoundError("Error: People.csv not found")

    # Process the CSV file
    try:
        result = update_people_from_csv(csv_file_path)
        print(f"File processed successfully: {result}")
    except Exception as e:
        raise RuntimeError(f"Error processing file: {str(e)}")


def update_people_from_csv(file_path):
    counts = {"updated_rows": 0, "new_rows":0,}
    try:
        with open(file_path, newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            session = create_session_from_str(create_enginestr_from_values(mysql))
            batch_size = (
                500  # Committing in batches causes less locks to be messed with
            )
            rows_processed = 0

            for row in reader:
                process_row(row, session, counts)
                rows_processed += 1

                if rows_processed % batch_size == 0:
                    session.commit()  # Commit after processing a batch of rows

            session.commit()  # Commit any remaining rows
            print(f"Committed remaining rows")

    except Exception as e:
        session.rollback()
        raise RuntimeError(f"Unexpected error: {str(e)}")
    finally:
        session.close()
    return counts


def process_row(row, session, counts):
    try:
        entry = People(
            playerID=row["playerID"],
            birthYear=(row["birthYear"] or None),
            birthMonth=(row["birthMonth"] or None),
            birthDay=(row["birthDay"] or None),
            birthCity=(row["birthCity"] or None),
            birthCountry=(row["birthCountry"] or None),
            birthState=(row["birthState"] or None),
            deathYear=(row["deathYear"] or None),
            deathMonth=(row["deathMonth"] or None),
            deathDay=(row["deathDay"] or None),
            deathCountry=(row["deathCountry"] or None),
            deathState=(row["deathState"] or None),
            deathCity=(row["deathCity"] or None),
            nameFirst=(row["nameFirst"] or None),
            nameLast=(row["nameLast"] or None),
            nameGiven=(row["nameGiven"] or None),
            weight=(int(row["weight"]) if row["weight"] else None),
            height=(int(row["height"]) if row["height"] else None),
            bats=(row["bats"] or None),
            throws=(row["throws"] or None),
            debutDate=(row["debut"] or None),
            finalGameDate=(row["finalGame"] or None),
        )

        with session.no_autoflush:
            existing_entry = (
                session.query(People)
                .filter_by(
                    playerID=entry.playerID
                )
                .first()
            )        
            
            if existing_entry:
                for column in People.__table__.columns:
                    # Skip the 'ID' column as it should not be modified
                    if column.name == 'playerID':
                        continue

                    updated = False
                    new_value = getattr(entry, column.name)
                    existing_value = getattr(existing_entry, column.name)

                    #skip if both columns are null
                    if new_value is None and existing_value is None:
                        continue

                    # If the values are different, update the existing record
                    if new_value != existing_value :
                        setattr(existing_entry, column.name, new_value)
                        updated = True

                    if updated:
                        counts["updated_rows"] += 1  # Only count as updated if something changed
            else:
                counts["new_rows"] += 1
                session.add(entry) 

            session.commit()
    except OperationalError as e:
        session.rollback()
        if "Deadlock found when trying to get lock" in str(e):
            print(f"Deadlock detected for row {row['playerID']}. Retrying...")
            process_row(row, session, counts)
        else:
            raise RuntimeError(f"Error processing row: {str(e)}")
