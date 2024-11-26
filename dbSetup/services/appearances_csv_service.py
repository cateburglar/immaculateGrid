import csv
import os
from multiprocessing import Pool
from models import Appearances, People, Teams
from utils import create_enginestr_from_values, create_session_from_str, get_csv_path
import csi3335f2024 as cfg

# Function to process a chunk of the CSV
def process_chunk(chunk_data):
    engine_str = create_enginestr_from_values(mysql=cfg.mysql)
    session = create_session_from_str(engine_str)
    new_rows, updated_rows, peopleNotExist, teamNotExists, skipCount = 0, 0, 0, 0, 0

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

        # Check for existing record
        if session.query(Appearances).filter_by(
            playerID=appearances_record.playerID,
            yearID=appearances_record.yearID,
            teamID=appearances_record.teamID,
        ).first():
            updated_rows += 1
        else:
            new_rows += 1

        session.merge(appearances_record)

    session.commit()
    session.close()
    return {
        "new_rows": new_rows,
        "updated_rows": updated_rows,
        "peopleNotExist": peopleNotExist,
        "teamNotExists": teamNotExists,
        "skipCount": skipCount,
    }

# Split CSV into chunks
def split_csv(file_path, chunksize=10000):
    with open(file_path, newline="") as csvfile:
        reader = list(csv.DictReader(csvfile))
        for i in range(0, len(reader), chunksize):
            yield reader[i:i + chunksize]

def upload_appearances_csv():
    print("Updating appearances table")
    csv_file_path = get_csv_path("Appearances.csv")
    if not os.path.exists(csv_file_path):
        print("Error: Appearances.csv not found")
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
        "skipCount": sum(r["skipCount"] for r in results),
    }

    print("Processing complete:", aggregated)


