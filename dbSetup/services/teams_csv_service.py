import csv

from csi3335f2024 import mysql
from models import Teams
from sqlalchemy.exc import SQLAlchemyError
from utils import create_enginestr_from_values, create_session_from_str, get_csv_path


def upload_teams_csv():
    print("Updating teams table")
    csv_file_path = get_csv_path("Teams.csv")

    if len(csv_file_path) == 0:
        raise FileNotFoundError("Error: Teams.csv not found")

    # Process the CSV file
    try:
        result = update_teams_from_csv(csv_file_path)
        print(f"File processed successfully: {result}")
    except Exception as e:
        raise RuntimeError(f"Error processing file: {str(e)}")


def update_teams_from_csv(file_path):
    try:
        with open(file_path, newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            session = create_session_from_str(create_enginestr_from_values(mysql))
            counts = {"updated_rows": 0, "new_rows": 0}
            # Process rows
            for row in reader:
                process_row(row, session, counts)
            # Commit updates
            session.commit()
    except (csv.Error, SQLAlchemyError) as e:
        session.rollback()
        raise RuntimeError(f"Error updating teams from CSV: {str(e)}")
    except Exception as e:
        raise RuntimeError(f"Unexpected error: {str(e)}")

    return counts


def process_row(row, session, counts):
    try:
        yearID = int(row["yearID"]) if row["yearID"] else None
        lgID = row["lgID"] or None
        teamID = row["teamID"] or None
        franchID = row["franchID"] or None
        team_name = row["name"] or None
        divID = row["divID"] or None
        team_rank = int(row["Rank"]) if row["Rank"] else None
        team_G = int(row["G"]) if row["G"] else None
        team_G_home = int(row["Ghome"]) if row["Ghome"] else None
        team_W = int(row["W"]) if row["W"] else None
        team_L = int(row["L"]) if row["L"] else None
        DivWin = row["DivWin"] or None
        WCWin = row["WCWin"] or None
        LgWin = row["LgWin"] or None
        WSWin = row["WSWin"] or None
        team_R = int(row["R"]) if row["R"] else None
        team_AB = int(row["AB"]) if row["AB"] else None
        team_H = int(row["H"]) if row["H"] else None
        team_2B = int(row["2B"]) if row["2B"] else None
        team_3B = int(row["3B"]) if row["3B"] else None
        team_HR = int(row["HR"]) if row["HR"] else None
        team_BB = int(row["BB"]) if row["BB"] else None
        team_SO = int(row["SO"]) if row["SO"] else None
        team_SB = int(row["SB"]) if row["SB"] else None
        team_CS = int(row["CS"]) if row["CS"] else None
        team_HBP = int(row["HBP"]) if row["HBP"] else None
        team_SF = int(row["SF"]) if row["SF"] else None
        team_RA = int(row["RA"]) if row["RA"] else None
        team_ER = int(row["ER"]) if row["ER"] else None
        team_ERA = float(row["ERA"]) if row["ERA"] else None
        team_CG = int(row["CG"]) if row["CG"] else None
        team_SHO = int(row["SHO"]) if row["SHO"] else None
        team_SV = int(row["SV"]) if row["SV"] else None
        team_IPouts = int(row["IPouts"]) if row["IPouts"] else None
        team_HA = int(row["HA"]) if row["HA"] else None
        team_HRA = int(row["HRA"]) if row["HRA"] else None
        team_BBA = int(row["BBA"]) if row["BBA"] else None
        team_SOA = int(row["SOA"]) if row["SOA"] else None
        team_E = int(row["E"]) if row["E"] else None
        team_DP = int(row["DP"]) if row["DP"] else None
        team_FP = float(row["FP"]) if row["FP"] else None
        park_name = row["park"] or None
        team_attendance = int(row["attendance"]) if row["attendance"] else None
        team_BPF = int(row["BPF"]) if row["BPF"] else None
        team_PPF = int(row["PPF"]) if row["PPF"] else None

        # Check if a row with the same yearID, lgID, and teamID exists
        existing_entry = (
            session.query(Teams)
            .filter_by(
                yearID=yearID,
                lgID=lgID,
                teamID=teamID,
            )
            .first()
        )

        if park_name and len(park_name) > 50:
            park_name = park_name[:50]

        if existing_entry:
            existing_entry.franchID = franchID
            existing_entry.team_name = team_name
            existing_entry.divID = divID
            existing_entry.team_ank = team_rank
            existing_entry.team_G = team_G
            existing_entry.team_G_home = team_G_home
            existing_entry.team_W = team_W
            existing_entry.team_L = team_L
            existing_entry.DivWin = DivWin
            existing_entry.WCWin = WCWin
            existing_entry.LgWin = LgWin
            existing_entry.WSWin = WSWin
            existing_entry.team_R = team_R
            existing_entry.team_AB = team_AB
            existing_entry.team_H = team_H
            existing_entry.team_2B = team_2B
            existing_entry.team_3B = team_3B
            existing_entry.team_HR = team_HR
            existing_entry.team_BB = team_BB
            existing_entry.team_SO = team_SO
            existing_entry.team_SB = team_SB
            existing_entry.team_CS = team_CS
            existing_entry.team_HBP = team_HBP
            existing_entry.team_SF = team_SF
            existing_entry.team_RA = team_RA
            existing_entry.team_ER = team_ER
            existing_entry.team_ERA = team_ERA
            existing_entry.team_CG = team_CG
            existing_entry.team_SHO = team_SHO
            existing_entry.team_SV = team_SV
            existing_entry.team_IPouts = team_IPouts
            existing_entry.team_HA = team_HA
            existing_entry.team_HRA = team_HRA
            existing_entry.team_BBA = team_BBA
            existing_entry.team_SOA = team_SOA
            existing_entry.team_E = team_E
            existing_entry.team_DP = team_DP
            existing_entry.team_FP = team_FP
            existing_entry.park_name = park_name
            existing_entry.team_attendance = team_attendance
            existing_entry.team_BPF = team_BPF
            existing_entry.team_PPF = team_PPF
            counts["updated_rows"] += 1
        else:
            # Insert a new record
            new_entry = Teams(
                yearID=yearID,
                lgID=lgID,
                teamID=teamID,
                franchID=franchID,
                name=team_name,
                divID=divID,
                Rank=team_rank,
                G=team_G,
                Ghome=team_G_home,
                W=team_W,
                L=team_L,
                DivWin=DivWin,
                WCWin=WCWin,
                LgWin=LgWin,
                WSWin=WSWin,
                R=team_R,
                AB=team_AB,
                H=team_H,
                **{"2B": team_2B, "3B": team_3B},
                HR=team_HR,
                BB=team_BB,
                SO=team_SO,
                SB=team_SB,
                CS=team_CS,
                HBP=team_HBP,
                SF=team_SF,
                RA=team_RA,
                ER=team_ER,
                ERA=team_ERA,
                CG=team_CG,
                SHO=team_SHO,
                SV=team_SV,
                IPouts=team_IPouts,
                HA=team_HA,
                HRA=team_HRA,
                BBA=team_BBA,
                SOA=team_SOA,
                E=team_E,
                DP=team_DP,
                FP=team_FP,
                park=park_name,
                attendance=team_attendance,
                BPF=team_BPF,
                PPF=team_PPF,
            )
            session.add(new_entry)
            counts["new_rows"] += 1
    except SQLAlchemyError as e:
        raise RuntimeError(f"Error processing row: {str(e)}")
