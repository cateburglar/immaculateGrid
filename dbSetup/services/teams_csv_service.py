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
            counts = {"updated_rows": 0}
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
        entry = Teams(
            yearID=(int(row["yearID"]) if row["yearID"] else None),
            lgID=(row["lgID"] or None),
            teamID=(row["teamID"] or None),
            franchID=(row["franchID"] or None),
            team_name=(row["name"] or None),
            divID=(row["divID"] or None),
            team_rank=(int(row["Rank"]) if row["Rank"] else None),
            team_G=(int(row["G"]) if row["G"] else None),
            team_G_home=(int(row["Ghome"]) if row["Ghome"] else None),
            team_W=(int(row["W"]) if row["W"] else None),
            team_L=(int(row["L"]) if row["L"] else None),
            DivWin=(row["DivWin"] or None),
            WCWin=(row["WCWin"] or None),
            LgWin=(row["LgWin"] or None),
            WSWin=(row["WSWin"] or None),
            team_R=(int(row["R"]) if row["R"] else None),
            team_AB=(int(row["AB"]) if row["AB"] else None),
            team_H=(int(row["H"]) if row["H"] else None),
            team_2B=(int(row["2B"]) if row["2B"] else None),
            team_3B=(int(row["3B"]) if row["3B"] else None),
            team_HR=(int(row["HR"]) if row["HR"] else None),
            team_BB=(int(row["BB"]) if row["BB"] else None),
            team_SO=(int(row["SO"]) if row["SO"] else None),
            team_SB=(int(row["SB"]) if row["SB"] else None),
            team_CS=(int(row["CS"]) if row["CS"] else None),
            team_HBP=(int(row["HBP"]) if row["HBP"] else None),
            team_SF=(int(row["SF"]) if row["SF"] else None),
            team_RA=(int(row["RA"]) if row["RA"] else None),
            team_ER=(int(row["ER"]) if row["ER"] else None),
            team_ERA=(float(row["ERA"]) if row["ERA"] else None),
            team_CG=(int(row["CG"]) if row["CG"] else None),
            team_SHO=(int(row["SHO"]) if row["SHO"] else None),
            team_SV=(int(row["SV"]) if row["SV"] else None),
            team_IPouts=(int(row["IPouts"]) if row["IPouts"] else None),
            team_HA=(int(row["HA"]) if row["HA"] else None),
            team_HRA=(int(row["HRA"]) if row["HRA"] else None),
            team_BBA=(int(row["BBA"]) if row["BBA"] else None),
            team_SOA=(int(row["SOA"]) if row["SOA"] else None),
            team_E=(int(row["E"]) if row["E"] else None),
            team_DP=(int(row["DP"]) if row["DP"] else None),
            team_FP=(float(row["FP"]) if row["FP"] else None),
            park_name=(row["park"] or None),
            team_attendance=(int(row["attendance"]) if row["attendance"] else None),
            team_BPF=(int(row["BPF"]) if row["BPF"] else None),
            team_PPF=(int(row["PPF"]) if row["PPF"] else None),
        )

        session.merge(entry)
        counts["updated_rows"] += 1
    except SQLAlchemyError as e:
        raise RuntimeError(f"Error processing row: {str(e)}")
