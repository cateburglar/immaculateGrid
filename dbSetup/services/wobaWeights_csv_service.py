import csv

import csi3335f2024 as cfg
from models import WobaWeights
from utils import create_enginestr_from_values, create_session_from_str, get_csv_path


def upload_wobaweights_csv():
    print("Updating wobaweights table")
    csv_file_path = get_csv_path("wobaWeights.csv")

    if len(csv_file_path) == 0:
        raise FileNotFoundError("Error: wobaWeights.csv not found")

    # Process the CSV file
    try:
        result = update_wobaWeights_from_csv(csv_file_path)
        print(f"File processed successfully: {result}")
    except Exception as e:
        raise RuntimeError(f"Error processing file: {str(e)}")


def update_wobaWeights_from_csv(file_path):
    with open(file_path, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        new_rows = 0

        # Create session
        session = create_session_from_str(create_enginestr_from_values(mysql=cfg.mysql))
        for row in reader:
            woba_record = WobaWeights(
                yearID=int(row["Season"]),
                League=float(row["League"]),
                wOBAScale=float(row["wOBAScale"]),
                wBB=float(row["wBB"]),
                wHBP=float(row["wHBP"]),
                w1B=float(row["w1B"]),
                w2B=float(row["w2B"]),
                w3B=float(row["w3B"]),
                wHR=float(row["wHR"]),
                runSB=float(row["runSB"]),
                runCS=float(row["runCS"]),
                R_PA=float(row["R/PA"]),
                R_W=float(row["R/W"]),
                cFIP=float(row["cFIP"]),
            )
            # only add record if it doesnt already exist
            if not (session.query(WobaWeights).filter_by(yearID = woba_record.yearID).first()):
                session.add(woba_record)
                new_rows +=1

        # Commit remaining batch
        session.commit()
        session.close()
    return {"new_rows": new_rows}
