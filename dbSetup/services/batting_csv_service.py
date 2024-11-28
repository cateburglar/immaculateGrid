import csv
import os
from multiprocessing import Pool
from models import Batting, People, Teams
from utils import create_enginestr_from_values, create_session_from_str, get_csv_path
import csi3335f2024 as cfg
from .processconfig import CHUNK_SIZE, NUM_PROCESSES

# Function to process a chunk of the CSV
def process_chunk(chunk_data):
    engine_str = create_enginestr_from_values(mysql=cfg.mysql)
    session = create_session_from_str(engine_str)
    new_rows, updated_rows, peopleNotExist, teamNotExists, = 0, 0, 0, 0

    for row in chunk_data:
        batting_record = Batting(
            playerID=row['playerID'],
            yearId=int(row['yearID']),
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

        # Check for existing record
        if session.query(Batting).filter_by(
            playerID=batting_record.playerID,
            yearId=batting_record.yearId,
            teamID=batting_record.teamID,
            stint=batting_record.stint
        ).first():
            updated_rows += 1
        else:
            new_rows += 1

        session.merge(batting_record)

    session.commit()
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

def upload_batting_csv():
    print("Updating batting table")
    csv_file_path = get_csv_path("Batting.csv")
    if not os.path.exists(csv_file_path):
        print("Error: Batting.csv not found")
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


