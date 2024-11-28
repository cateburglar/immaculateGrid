import csv
import os
from multiprocessing import Pool
import time
from functools import wraps
from sqlalchemy.exc import OperationalError, SQLAlchemyError
from models import Batting, People, Teams
from utils import create_enginestr_from_values, create_session_from_str, get_csv_path
import csi3335f2024 as cfg

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
    new_rows, updated_rows, peopleNotExist, teamNotExists, = 0, 0, 0, 0
    batch_counter, batch_size = 0, 500

    try:
        for row in chunk_data:
            batting_record = Batting(
                playerID=row['playerID'],
                yearID=int(row['yearID']),
                stint=int(row['stint']),
                teamID=row['teamID'].strip(),
                b_G=int(row['G']) if row['G'] else None,
                b_AB=int(row['AB']) if row['AB'] else None,
                b_R=int(row['R']) if row['R'] else None,
                b_H=int(row['H']) if row['H'] else None,
                b_2B=int(row['2B']) if row['2B'] else None,
                b_3B=int(row['3B']) if row['3B'] else None,
                b_HR=int(row['HR']) if row['HR'] else None,
                b_RBI=int(row['RBI']) if row['RBI'] else None,
                b_SB=int(row['SB']) if row['SB'] else None,
                b_CS=int(row['CS']) if row['CS'] else None,
                b_BB=int(row['BB']) if row['BB'] else None,
                b_SO=int(row['SO']) if row['SO'] else None,
                b_IBB=int(row['IBB']) if row['IBB'] else None,
                b_HBP=int(row['HBP']) if row['HBP'] else None,
                b_SH=int(row['SH']) if row['SH'] else None,
                b_SF=int(row['SF']) if row['SF'] else None,
                b_GIDP=int(row['GIDP']) if row['GIDP'] else None,
            )

            # Check if playerID exists
            if not session.query(People).filter_by(playerID=batting_record.playerID).first():
                peopleNotExist += 1
                continue

            # Check if teamID exists
            if not session.query(Teams).filter_by(teamID=batting_record.teamID).first():
                teamNotExists += 1
                continue

            existing_record = session.query(Batting).filter_by(
                playerID=batting_record.playerID,
                yearID=batting_record.yearID,
                teamID=batting_record.teamID,
                stint=batting_record.stint
            ).first()

            # Check for existing record
            if existing_record:
                for column in Batting.__table__.columns:
                    # Skip the 'ID' column as it should not be modified
                    if column.name == 'batting_ID':
                        continue

                    updated = False
                    new_value = getattr(batting_record, column.name)
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
                session.add(batting_record)
        
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
def split_csv(file_path, chunksize=10000):
    with open(file_path, newline="") as csvfile:
        reader = list(csv.DictReader(csvfile))
        for i in range(0, len(reader), chunksize):
            # Yield a slice of reader list from index i to i+chunksize
            # <start>:<end>
            yield reader[i:i + chunksize]

def upload_batting_csv():
    print("Updating batting table")
    csv_file_path = get_csv_path("Batting.csv")
    if not os.path.exists(csv_file_path):
        print("Error: Batting.csv not found")
        return

    chunks = list(split_csv(csv_file_path))

    # Use multiprocessing to process chunks
    with Pool(processes=os.cpu_count()) as pool:
        results = pool.map(process_chunk, chunks)

    # Aggregate results
    aggregated = {
        "new rows": sum(r["new_rows"] for r in results),
        "updated rows": sum(r["updated_rows"] for r in results),
        "peopleNotExist": sum(r["peopleNotExist"] for r in results),
        "teamNotExists": sum(r["teamNotExists"] for r in results),
    }

    print("Processing complete:", aggregated)


