import csv

import dbSetup.csi3335f2024 as cfg
from dbSetup.models import Pitching, People
from dbSetup.utils import create_enginestr_from_values, create_session_from_str, get_csv_path


def upload_pitching_csv():
    print("Updating pitching table")
    csv_file_path = get_csv_path("Pitching.csv")

    if len(csv_file_path) == 0:
        print("Error: Pitching.csv not found")
        return

    # Process the CSV file
    try:
        print(update_pitching_from_csv(csv_file_path))
        print("File processed successfully")
    except Exception as e:
        print(f"Error: {str(e)}")


def update_pitching_from_csv(file_path):
    with open(file_path, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        new_rows = 0
        updated_rows = 0

        # Create session
        session = create_session_from_str(create_enginestr_from_values(mysql=cfg.mysql))

        for row in reader:
            pitching_record = Pitching(
                playerID=row['playerID'],
                yearID=int(row['yearID']),
                teamID=row['teamID'],
                stint=int(row['stint']),
                p_W=int(row['p_W']) if row['p_W'] else None,
                p_L=int(row['p_L']) if row['p_L'] else None,
                p_G=int(row['p_G']) if row['p_G'] else None,
                p_GS=int(row['p_GS']) if row['p_GS'] else None,
                p_CG=int(row['p_CG']) if row['p_CG'] else None,
                p_SHO=int(row['p_SHO']) if row['p_SHO'] else None,
                p_SV=int(row['p_SV']) if row['p_SV'] else None,
                p_IPOuts=int(row['p_IPOuts']) if row['p_IPOuts'] else None,
                p_H=int(row['p_H']) if row['p_H'] else None,
                p_ER=int(row['p_ER']) if row['p_ER'] else None,
                p_BB=int(row['p_BB']) if row['p_BB'] else None,
                p_SO=int(row['p_SO']) if row['p_SO'] else None,
                p_BAOpp=float(row['p_BAOpp']) if row['p_BAOpp'] else None,
                p_ERA=float(row['p_ERA']) if row['p_ERA'] else None,
                p_IBB=int(row['p_IBB']) if row['p_IBB'] else None,
                p_WP=int(row['p_WP']) if row['p_WP'] else None,
                p_HBP=int(row['p_HBP']) if row['p_HBP'] else None,
                p_BK=int(row['p_BK']) if row['p_BK'] else None,
                p_BFP=int(row['p_BFP']) if row['p_BFP'] else None,
                p_GF=int(row['p_GF']) if row['p_GF'] else None,
                p_R=int(row['p_R']) if row['p_R'] else None,
                p_SH=int(row['p_SH']) if row['p_SH'] else None,
                p_SF=int(row['p_SF']) if row['p_SF'] else None,
                p_GIDP=int(row['p_GIDP']) if row['p_GIDP'] else None
            )

            # Check if playerID exists in the people table
            player_exists = session.query(People).filter_by(playerID=pitching_record.playerID).first()

            if not player_exists:
                print(
                    f"playerID {pitching_record.playerID} does not exist in the people table. Skipping row."
                )
                continue


            # Check if a row with the same playerID, yearID, teamID, and stint exists
            existing_entry = (
                session.query(Pitching)
                .filter_by(
                    playerID=pitching_record.playerID,
                    yearID=pitching_record.yearID,
                    teamID=pitching_record.teamID,
                    stint=pitching_record.stint,
                )
                .first()
            )

            if existing_entry:
                print(
                    f"error- playerID {pitching_record.playerID} already exists. Skipping row."
                )
                continue
            else:
                # Insert a new record
                new_entry = Pitching(
                    playerID=pitching_record.playerID,
                    yearID=pitching_record.yearID,
                    teamID=pitching_record.teamID,
                    pitchingID= pitching_record.pitchingID,
                    stint = pitching_record.stint,
                    p_W = pitching_record.p_W,
                    p_L = pitching_record.p_L,
                    p_G = pitching_record.p_G,
                    p_GS = pitching_record.p_GS,
                    p_CG = pitching_record.p_CG,
                    p_SHO = pitching_record.p_SHO,
                    p_SV = pitching_record.p_SV,
                    p_IPOuts = pitching_record.p_IPOuts,
                    p_H = pitching_record.p_H,
                    p_ER = pitching_record.p_ER,
                    p_BB = pitching_record.p_BB,
                    p_SO = pitching_record.p_SO,
                    p_BAOpp = pitching_record.p_BAOpp,
                    p_ERA = pitching_record.p_ERA,
                    p_IBB = pitching_record.p_IBB,
                    p_WP = pitching_record.p_WP,
                    p_HBP = pitching_record.p_HBP,
                    p_BK = pitching_record.p_BK,
                    p_BFP = pitching_record.p_BFP,
                    p_GF =pitching_record.p_GF,
                    p_R = pitching_record.p_R,
                    p_SH = pitching_record.p_SH,
                    p_SF =pitching_record.p_SF,
                    p_GIDP =pitching_record.p_GIDP,
                )
                session.add(new_entry)
                new_rows += 1

            session.commit()

    session.close()
    return {"new_rows": new_rows, "updated_rows": updated_rows}
