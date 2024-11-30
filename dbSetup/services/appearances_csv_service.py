import csv
import os
import time
from functools import wraps
from multiprocessing import Pool
from sqlalchemy.exc import OperationalError, SQLAlchemyError
from models import Appearances, People, Teams
from utils import create_enginestr_from_values, create_session_from_str, get_csv_path
import csi3335f2024 as cfg
from .processconfig import CHUNK_SIZE, NUM_PROCESSES

# Retry decorator for deadlock handling
def retry_on_deadlock(tries=3, delay=2):
    """Decorator to retry a function if a deadlock occurs."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            attempt = 0
            while attempt < tries:
                try:
                    return func(*args, **kwargs)
                except OperationalError as e:
                    if "Deadlock" in str(e):
                        attempt += 1
                        print(f"Deadlock detected. Retrying ({attempt}/{tries})...")
                        time.sleep(delay)
                        if attempt == tries:
                            print("Max retries reached. Raising exception.")
                            raise
                    else:
                        raise  # Other OperationalErrors are re-raised
        return wrapper
    return decorator



# Function to process a chunk of the CSV
#the function will try 3 times to execute successfully before giving up.
#the function will wait 2 seconds before retrying if a deadlock occurs.
@retry_on_deadlock(tries=3, delay=2)
def process_chunk(chunk_data):
    engine_str = create_enginestr_from_values(mysql=cfg.mysql)
    session = create_session_from_str(engine_str)
    new_rows, updated_rows, peopleNotExist, teamNotExists = 0, 0, 0, 0
    batch_counter, batch_size = 0, 100

    try:
        for row in chunk_data:
            appearances_record = Appearances(
                playerID=row["playerID"],
                yearID=int(row["yearID"]),
                teamID=row["teamID"],
                G_all=row["G_all"] or None,
                GS=row["GS"] or None,
                G_batting=row["G_batting"] or None,
                G_defense=row["G_defense"] or None,
                G_p=row["G_p"] or None,
                G_c=row["G_c"] or None,
                G_1b=row["G_1b"] or None,
                G_2b=row["G_2b"] or None,
                G_3b=row["G_3b"] or None,
                G_ss=row["G_ss"] or None,
                G_lf=row["G_lf"] or None,
                G_cf=row["G_cf"] or None,
                G_rf=row["G_rf"] or None,
                G_of=row["G_of"] or None,
                G_dh=row["G_dh"] or None,
                G_ph=row["G_ph"] or None,
                G_pr=row["G_pr"] or None,
            )

            # Check if playerID exists
            if not session.query(People).filter_by(playerID=appearances_record.playerID).first():
                peopleNotExist += 1
                continue

            # Check if teamID exists
            if not session.query(Teams).filter_by(teamID=appearances_record.teamID).first():
                teamNotExists += 1
                continue

            # Check for existing record (duplicates)
            existing_record = session.query(Appearances).filter_by(
                playerID=appearances_record.playerID,
                yearID=appearances_record.yearID,
                teamID=appearances_record.teamID,
            ).first()

            if existing_record:
                for column in Appearances.__table__.columns:
                    # Skip the 'appearances_ID' column as it should not be modified
                    if column.name == 'appearances_ID':
                        continue

                    updated = False
                    new_value = getattr(appearances_record, column.name)
                    existing_value = getattr(existing_record, column.name)

                    #skip if both columns are null
                    if new_value is None and existing_value is None:
                        continue

                    # If the values are different, update the existing record
                    if existing_value is None or new_value != existing_value :
                        setattr(existing_record, column.name, new_value)
                        updated = True

                if updated:
                    updated_rows += 1  # Only count as updated if something changed
            else:
                new_rows += 1
                session.add(appearances_record)  # Add the new record

            batch_counter += 1

            # Commit in batches
            if batch_counter >= batch_size:
                session.commit()
                batch_counter = 0

        # Commit remaining batch
        session.commit()
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Error occurred during processing: {e._message}")
    finally:
        session.close()

    return {
        "new_rows": new_rows,
        "updated_rows": updated_rows,
        "peopleNotExist": peopleNotExist,
        "teamNotExists": teamNotExists,
    }

# Split CSV into chunks
def split_csv(file_path, chunksize=CHUNK_SIZE):
    with open(file_path, newline="") as csvfile:
        reader = list(csv.DictReader(csvfile))
        for i in range(0, len(reader), chunksize):
            # Yield a slice of reader list from index i to i+chunksize
            # <start>:<end>
            yield reader[i:i + chunksize]

def upload_appearances_csv():
    print("Updating appearances table")
    csv_file_path = get_csv_path("Appearances.csv")
    if not os.path.exists(csv_file_path):
        print("Error: Appearances.csv not found")
        return

    chunks = list(split_csv(csv_file_path))

    # Use multiprocessing to process chunks
    with Pool(processes=NUM_PROCESSES) as pool:
        results = pool.map(process_chunk, chunks)

    # Aggregate results
    aggregated = {
        "new rows": sum(r["new_rows"] for r in results),
        "updated rows": sum(r["updated_rows"] for r in results),
        "peopleNotExist": sum(r["peopleNotExist"] for r in results),
        "teamNotExists": sum(r["teamNotExists"] for r in results),
    }

    print("Processing complete:", aggregated)


