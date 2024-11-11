import csv

import csi3335f2024 as cfg
from models import Pitching, People
from utils import create_enginestr_from_values, create_session_from_str, get_csv_path


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
        skipCount=0
        peopleNotExist=0
        for row in reader:
            pitching_record = Pitching(
                playerID=row['playerID'],
                yearID=int(row['yearID']),
                teamID=row['teamID'],
                stint=int(row['stint']),
                p_W=int(row['W']) if row['W'] else None,
                p_L=int(row['L']) if row['L'] else None,
                p_G=int(row['G']) if row['G'] else None,
                p_GS=int(row['GS']) if row['GS'] else None,
                p_CG=int(row['CG']) if row['CG'] else None,
                p_SHO=int(row['SHO']) if row['SHO'] else None,
                p_SV=int(row['SV']) if row['SV'] else None,
                p_IPouts=int(row['IPouts']) if row['IPouts'] else None,
                p_H=int(row['H']) if row['H'] else None,
                p_ER=int(row['ER']) if row['ER'] else None,
                p_BB=int(row['BB']) if row['BB'] else None,
                p_SO=int(row['SO']) if row['SO'] else None,
                p_BAOpp=float(row['BAOpp']) if row['BAOpp'] else None,
                p_ERA=float(row['ERA']) if row['ERA'] else None,
                p_IBB=int(row['IBB']) if row['IBB'] else None,
                p_WP=int(row['WP']) if row['WP'] else None,
                p_HBP=int(row['HBP']) if row['HBP'] else None,
                p_BK=int(row['BK']) if row['BK'] else None,
                p_BFP=int(row['BFP']) if row['BFP'] else None,
                p_GF=int(row['GF']) if row['GF'] else None,
                p_R=int(row['R']) if row['R'] else None,
                p_SH=int(row['SH']) if row['SH'] else None,
                p_SF=int(row['SF']) if row['SF'] else None,
                p_GIDP=int(row['GIDP']) if row['GIDP'] else None
            )

            # Check if playerID exists in the people table
            player_exists = session.query(People).filter_by(playerID=pitching_record.playerID).first()

            if not player_exists:
                peopleNotExist+=1
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
                skipCount+=1
                #print(
                #    f"error- row with matching playerid, yearid, teamid, and stint for playerID {pitching_record.playerID} already exists. Skipping row."
                #)
                continue
            else:
                # Insert a new record
                new_entry = Pitching(
                    playerID=pitching_record.playerID,
                    yearID=pitching_record.yearID,
                    teamID=pitching_record.teamID,
                    stint = pitching_record.stint,
                    p_W = pitching_record.p_W,
                    p_L = pitching_record.p_L,
                    p_G = pitching_record.p_G,
                    p_GS = pitching_record.p_GS,
                    p_CG = pitching_record.p_CG,
                    p_SHO = pitching_record.p_SHO,
                    p_SV = pitching_record.p_SV,
                    p_IPouts = pitching_record.p_IPouts,
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
        print(f"{skipCount} rows with matching teamids, yearids, stints, and playerids existed. skipped those rows.")
        print(f"{peopleNotExist} people were skipped because they didn't exist in people table")
    session.close()
    return {"new_rows": new_rows, "updated_rows": updated_rows}
