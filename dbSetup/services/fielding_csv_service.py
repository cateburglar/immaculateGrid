import csv
import os
from multiprocessing import Pool
import time
from functools import wraps
from sqlalchemy.exc import OperationalError, SQLAlchemyError
from models import Fielding, People, Teams
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
    new_rows, updated_rows, peopleNotExist, teamNotExists, =  0,0,0,0
    batch_counter, batch_size = 0, 500

    try:
        for row in chunk_data:
            fielding_record = Fielding(
                playerID=row['playerID'],
                yearID=int(row['yearID']),
                teamID=row['teamID'],
                stint=int(row['stint']),
                position=row['POS'] if row['POS'] else None,
                f_G=int(row['G']) if row['G'] else None,
                f_GS=int(row['GS']) if row['GS'] else None,
                f_InnOuts=int(row['InnOuts']) if row['InnOuts'] else None,
                f_PO=int(row['PO']) if row['PO'] else None,
                f_A=int(row['A']) if row['A'] else None,
                f_E=int(row['E']) if row['E'] else None,
                f_DP=int(row['DP']) if row['DP'] else None,
                f_PB=int(row['PB']) if row['PB'] else None,
                f_WP=int(row['WP']) if row['WP'] else None,
                f_SB=int(row['SB']) if row['SB'] else None,
                f_CS=int(row['CS']) if row['CS'] else None,
                f_ZR=float(row['ZR']) if row['ZR'] else None,
            )

            # Check if playerID exists
            if not session.query(People).filter_by(playerID=fielding_record.playerID).first():
                peopleNotExist += 1
                continue

            # Check if teamID exists
            if not session.query(Teams).filter_by(teamID=fielding_record.teamID).first():
                teamNotExists += 1
                continue
            

            existing_record = session.query(Fielding).filter_by(
                playerID=fielding_record.playerID,
                yearID=fielding_record.yearID,
                teamID=fielding_record.teamID,
                stint=fielding_record.stint,
                position=fielding_record.position,
            ).first()

            # Check for existing record
            if existing_record:
                for column in Fielding.__table__.columns:
                    # Skip the 'ID' column as it should not be modified
                    if column.name == 'fielding_ID':
                        continue

                    updated = False
                    new_value = getattr(fielding_record, column.name)
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
                session.add(fielding_record)
        
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

def upload_fielding_csv():
    print("Updating fielding table")
    csv_file_path = get_csv_path("Fielding.csv")
    if not os.path.exists(csv_file_path):
        print("Error: Fielding.csv not found")
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


