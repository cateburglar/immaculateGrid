import csv

import csi3335f2024 as cfg
from models import Baseball
from utils import create_enginestr_from_values, create_session_from_str, get_csv_path

def upload_baseball_csv():
    csv_file_path = get_csv_path("Baseball.csv")

    if len(csv_file_path) == 0:
        print("Error: Baseball.csv not found")
        return

    # Process CSV
    try:
        print(update_baseball_from_csv(csv_file_path))
        print("File processesed successfully")
    except Exception as e:
        print(f"Error: {str(e)}")

def update_baseball_from_csv(file_path):
    with open(file_path, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        new_rows = 0
        updated_rows = 0

        # Create session
        for row in reader:
            # Convert empty strings to None
            batting_ID = row["batting_ID"]
            playerID = row["playerID"]
            yearId = row["yearId"]
            teamID = row["teamID"]
            stint = row["stint"]
            b_G = row["b_G"]
            b_AB = row["b_AB"]
            b_R = row["b_R"]
            b_H = row["b_H"]
            b_2B = row["b_2B"]
            b_3B = row["b_3B"]
            b_HR = row["b_HR"]
            b_RBI = row["b_RBI"]
            b_SB = row["b_SB"]
            b_CS = row["b_CS"]
            b_BB = row["b_BB"]
            b_SO = row["b_SO"]
            b_IBB = row["b_IBB"]
            b_HBP = row["b_HBP"]
            b_SH = row["b_SH"]
            b_SF = row["b_SF"]
            b_GIDP = row["b_GIDP"]

            # Debug prints
            # print(f"Processing row: playerID={playerID}")

            # Check if playerID exists in the people table
            batting_exists = session.query(Baseball).filter_by(playerID=playerID).first()

            if batting_exists:
                # Update the existing record
                batting_exists.playerID = playerID
                batting_exists.yearId = yearId
                batting_exists.teamID = teamID
                batting_exists.stint = stint
                batting_exists.b_G = b_G
                batting_exists.b_AB = b_AB
                batting_exists.b_R = b_R
                batting_exists.b_H = b_H
                batting_exists.b_2B = b_2B
                batting_exists.b_3B = b_3B
                batting_exists.b_HR = b_HR
                batting_exists.b_RBI = b_RBI
                batting_exists.b_SB = b_SB
                batting_exists.b_CS = b_CS
                batting_exists.b_BB = b_BB
                batting_exists.b_SO = b_SO
                batting_exists.b_IBB = b_IBB
                batting_exists.b_HBP = b_HBP
                batting_exists.b_SH = b_SH
                batting_exists.b_SF = b_SF
                batting_exists.b_GIDP = b_GIDP
                updated_rows += 1
            else:
                # Insert a new record
                new_entry = Baseball(
                    playerID = playerID,
                    yearId = yearId,
                    teamID = teamID,
                    stint = stint,
                    b_G = b_G,
                    b_AB = b_AB,
                    b_R = b_R,
                    b_H = b_H,
                    b_2B = b_2B,
                    b_3B = b_3B,
                    b_HR = b_HR,
                    b_RBI = b_RBI,
                    b_SB = b_SB,
                    b_CS = b_CS,
                    b_BB = b_BB,
                    b_SO = b_SO,
                    b_IBB = b_IBB,
                    b_HBP = b_HBP,
                    b_SH = b_SH,
                    b_SF = b_SF,
                    b_GIDP = b_GIDP
                )
                session.add(new_entry)
                new_rows += 1

        session.commit()

        session.close()
        return {"new_rows": new_rows, "updated_rows": updated_rows}
