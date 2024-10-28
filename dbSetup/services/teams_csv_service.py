import csv

import csi3335f2024 as cfg
from models import Leagues, Teams
from utils import create_enginestr_from_values, create_session_from_str, get_csv_path


def upload_teams_csv():
    csv_file_path = get_csv_path("Teams.csv")

    if len(csv_file_path) == 0:
        print("Error: Teams.csv not found")
        return

    # Process the CSV file
    try:
        print(update_teams_from_csv(csv_file_path))
        print("File processed successfully")
    except Exception as e:
        print(f"Error: {str(e)}")


def update_teams_from_csv(file_path):
    with open(file=file_path, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        new_rows = 0
        updated_rows = 0

        # Create session
        session = create_session_from_str(create_enginestr_from_values(cfg.mysql))

        # Parse each row
        for row in reader:
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

            # Make sure FK isn't violated
            lg_exists = session.query(Leagues).filter_by(lgID=lgID).first()
            if not lg_exists:
                print(f"lgID {lgID} does not exist in the leagues table. Skipping row.")
                continue

            # Check if team already exists
            existing_entry = (
                session.query(Teams)
                .filter_by(
                    teamID=teamID,
                    yearID=yearID,
                    lgID=lgID,
                )
                .first()
            )

            if park_name and len(park_name) > 50:
                park_name = park_name[:50]

            if existing_entry:
                # Calculate projected wins
                if (
                    team_R is not None
                    and team_RA is not None
                    and team_R > 0
                    and team_RA > 0
                ):
                    team_projW = round(
                        (pow(team_R, 2) / (pow(team_R, 2) + pow(team_RA, 2))) * team_G,
                        0,
                    )
                else:
                    team_projW = None

                # Calculate projected losses
                if team_projW is not None and team_G is not None and team_G > 0:
                    team_projL = team_G - team_projW
                else:
                    team_projL = None

                existing_entry.lgID = lgID
                existing_entry.divID = divID
                existing_entry.team_name = team_name
                existing_entry.team_rank = team_rank
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
                existing_entry.team_projW = team_projW
                existing_entry.team_projL = team_projL
                updated_rows += 1

            if not existing_entry:

                # Calculate projected wins
                if (
                    team_R is not None
                    and team_RA is not None
                    and team_R > 0
                    and team_RA > 0
                ):
                    team_projW = round(
                        (pow(team_R, 2) / (pow(team_R, 2) + pow(team_RA, 2))) * team_G,
                        0,
                    )
                else:
                    team_projW = None

                # Calculate projected losses
                if team_projW is not None and team_G is not None and team_G > 0:
                    team_projL = team_G - team_projW
                else:
                    team_projL = None

                new_entry = Teams(
                    yearID=yearID,
                    lgID=lgID,
                    teamID=teamID,
                    franchID=franchID,
                    divID=divID,
                    team_name=team_name,
                    team_rank=team_rank,
                    team_G=team_G,
                    team_G_home=team_G_home,
                    team_W=team_W,
                    team_L=team_L,
                    DivWin=DivWin,
                    WCWin=WCWin,
                    LgWin=LgWin,
                    WSWin=WSWin,
                    team_R=team_R,
                    team_AB=team_AB,
                    team_H=team_H,
                    team_2B=team_2B,
                    team_3B=team_3B,
                    team_HR=team_HR,
                    team_BB=team_BB,
                    team_SO=team_SO,
                    team_SB=team_SB,
                    team_CS=team_CS,
                    team_HBP=team_HBP,
                    team_SF=team_SF,
                    team_RA=team_RA,
                    team_ER=team_ER,
                    team_ERA=team_ERA,
                    team_CG=team_CG,
                    team_SHO=team_SHO,
                    team_SV=team_SV,
                    team_IPouts=team_IPouts,
                    team_HA=team_HA,
                    team_HRA=team_HRA,
                    team_BBA=team_BBA,
                    team_SOA=team_SOA,
                    team_E=team_E,
                    team_DP=team_DP,
                    team_FP=team_FP,
                    park_name=park_name,
                    team_attendance=team_attendance,
                    team_BPF=team_BPF,
                    team_PPF=team_PPF,
                    team_projW=team_projW,
                    team_projL=team_projL,
                )
                session.add(new_entry)
                new_rows += 1

            session.commit()

        session.close()
        return {"new_rows": new_rows, "updated rows": updated_rows}
