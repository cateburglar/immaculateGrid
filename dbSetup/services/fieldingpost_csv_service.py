import csv
import time
from functools import wraps
from sqlalchemy.exc import OperationalError, SQLAlchemyError
import csi3335f2024 as cfg
from models import FieldingPost, People, Teams
from utils import create_enginestr_from_values, create_session_from_str, get_csv_path


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
def upload_fieldingpost_csv():
    print("Updating fielding post table")
    csv_file_path = get_csv_path("FieldingPost.csv")

    if len(csv_file_path) == 0:
        print("Error: FieldingPost.csv not found")
        return

    # Process the CSV file
    try:
        print(update_fieldingpost_from_csv(csv_file_path))
        print("File processed successfully")
    except Exception as e:
        print(f"Error: {str(e)}")


def update_fieldingpost_from_csv(file_path):
    with open(file_path, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        new_rows = 0
        updated_rows = 0
        peopleNotExist=0
        teamNotExist=0
        batch_size = 500
        batch_counter = 0

        # Create session
        session = create_session_from_str(create_enginestr_from_values(mysql=cfg.mysql))
        try:
            for row in reader:
                fieldingpost_record = FieldingPost(
                    playerID=row['playerID'],
                    yearID=int(row['yearID']),
                    teamID=row['teamID'],
                    round=row['round'],
                    position=row['POS'] if row['POS'] else None,
                    f_G=int(row['G']) if row['G'] else None,
                    f_GS=int(row['GS']) if row['GS'] else None,
                    f_InnOuts=int(row['InnOuts']) if row['InnOuts'] else None,
                    f_PO=int(row['PO']) if row['PO'] else None,
                    f_A=int(row['A']) if row['A'] else None,
                    f_E=int(row['E']) if row['E'] else None,
                    f_DP=int(row['DP']) if row['DP'] else None,
                    f_TP=int(row['TP']) if row['TP'] else None,
                    f_PB=int(row['PB']) if row['PB'] else None,

                    # SB and CS are not present in our database
                    # although they exist in the CSV file
                    # f_SB=int(row['SB']) if row['SB'] else None,
                    # f_CS=int(row['CS']) if row['CS'] else None,
                )

                # Check if playerID exists in the people table
                player_exists = session.query(People).filter_by(playerID=fieldingpost_record.playerID).first()

                if not player_exists:
                    peopleNotExist+=1
                    #if we make an error log, message could go here.
                    continue

                #check if teamid exists in teams table
                team_exists = session.query(Teams).filter_by(teamID=fieldingpost_record.teamID).first()
                
                if not team_exists:
                    teamNotExist+=1
                    #if we make an error log, a message could go here.
                    continue

                # Check if a row with the same playerID, yearID, teamID, and round exists
                existing_entry = (
                    session.query(FieldingPost)
                    .filter_by(
                        playerID=fieldingpost_record.playerID,
                        yearID=fieldingpost_record.yearID,
                        teamID=fieldingpost_record.teamID,
                        round=fieldingpost_record.round,
                    )
                    .first()
                )

                # Check for existing record
                if existing_entry:
                    for column in FieldingPost.__table__.columns:
                        # Skip the 'ID' column as it should not be modified
                        if column.name == 'fieldingpost_ID':
                            continue

                        updated = False
                        new_value = getattr(fieldingpost_record, column.name)
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
                    session.add(fieldingpost_record)
            
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
        "new rows": new_rows,
        "updated rows: ": updated_rows,
        "rows skipped bc their playerid didn't exist in people table: ": peopleNotExist, 
        "rows skipped bc their teamid didnt exist in teams table: ": teamNotExist
    }
