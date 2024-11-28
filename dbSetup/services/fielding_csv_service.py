import csv
import os
from multiprocessing import Pool
from models import Fielding, People, Teams
from utils import create_enginestr_from_values, create_session_from_str, get_csv_path
import csi3335f2024 as cfg
from processconfig import CHUNK_SIZE, NUM_PROCESSES

# Function to process a chunk of the CSV
def process_chunk(chunk_data):
    engine_str = create_enginestr_from_values(mysql=cfg.mysql)
    session = create_session_from_str(engine_str)
    new_rows, updated_rows, peopleNotExist, teamNotExists, = 0, 0, 0, 0

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

        # Check for existing record
        if session.query(Fielding).filter_by(
            playerID=fielding_record.playerID,
            yearID=fielding_record.yearID,
            teamID=fielding_record.teamID,
            stint=fielding_record.stint
        ).first():
            updated_rows += 1
        else:
            new_rows += 1

        session.merge(fielding_record)

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


