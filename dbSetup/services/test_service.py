import csi3335f2024 as cfg
from models import AllstarFull, People, Schools, Teams
from utils import create_enginestr_from_values, create_session_from_str


def compare_existing_allstarfull_entries():

    # Create sessions
    sq_session = create_session_from_str(create_enginestr_from_values(cfg.mysql))
    bb_session = create_session_from_str(
        create_enginestr_from_values(cfg.baseballmysql)
    )

    # Get the original AllstarFull rows
    bb_result = bb_session.query(AllstarFull).all()

    # Go through each row in the original baseball database to make sure ours matches
    rows_match = True
    for row in bb_result:
        row_exists = sq_session.query(AllstarFull).filter_by(
            allstarfull_ID=row.allstarfull_ID,
            playerID=row.playerID,
            yearID=row.yearID,
            lgID=row.lgID,
            teamID=row.teamID,
            gameID=row.gameID,
            GP=row.GP,
            startingPos=row.startingPos,
        )

        # Alert that test failed, and for what row
        if not row_exists:
            print(
                f"Row could not be found for: playerid={row.playerID}, yearid={row.yearID}, lgID={row.lgID}, teamID={row.teamID}"
            )
            rows_match = False

    # Commit and close sessions
    sq_session.commit()
    sq_session.close()
    bb_session.commit()
    bb_session.close()

    # Output test result
    if not rows_match:
        return "FAILURE: allstarfull"
    else:
        return ""


def compare_existing_people_entries():

    # Create sessions
    sq_session = create_session_from_str(create_enginestr_from_values(cfg.mysql))
    bb_session = create_session_from_str(
        create_enginestr_from_values(cfg.baseballmysql)
    )

    # Get all rows from the original People table
    bb_result = bb_session.query(People).all()

    # Go through each row in the original baseball database to make sure ours matches
    rows_match = True
    for row in bb_result:
        row_exists = (
            sq_session.query(People)
            .filter_by(
                playerID=row.playerID,
                birthYear=row.birthYear,
                birthMonth=row.birthMonth,
                birthDay=row.birthDay,
                birthCity=row.birthCity,
                birthCountry=row.birthCountry,
                birthState=row.birthState,
                deathYear=row.deathYear,
                deathMonth=row.deathMonth,
                deathDay=row.deathDay,
                deathCountry=row.deathCountry,
                deathState=row.deathState,
                deathCity=row.deathCity,
                nameFirst=row.nameFirst,
                nameLast=row.nameLast,
                nameGiven=row.nameGiven,
                weight=row.weight,
                height=row.height,
                bats=row.bats,
                throws=row.throws,
                debutDate=row.debutDate,
                finalGameDate=row.finalGameDate,
            )
            .first()
        )

        # Alert that test failed, and for what row
        if not row_exists:
            print(f"Row does match for: playerid={row.playerID}")
            rows_match = False

    # Commit and close sessions
    sq_session.commit()
    sq_session.close()
    bb_session.commit()
    bb_session.close()

    # Output test result
    if not rows_match:
        return "FAILURE: people"
    else:
        return ""


def compare_existing_teams_entries():
    # Create sessions
    sq_session = create_session_from_str(create_enginestr_from_values(cfg.mysql))
    bb_session = create_session_from_str(
        create_enginestr_from_values(cfg.baseballmysql)
    )

    # Get all rows from the original People table
    bb_result = bb_session.query(Teams).all()

    # Go through each row in the original baseball database to make sure ours matches
    rows_match = True
    for row in bb_result:
        row_exists = (
            sq_session.query(Teams)
            .filter_by(
                yearID=row.yearID,
                lgID=row.lgID,
                teamID=row.teamID,
                franchID=row.franchID,
                divID=row.divID,
                team_name=row.team_name,
                team_rank=row.team_rank,
                team_G=row.team_G,
                team_G_home=row.team_G_home,
                team_W=row.team_W,
                team_L=row.team_L,
                DivWin=row.DivWin,
                WCWin=row.WCWin,
                LgWin=row.LgWin,
                WSWin=row.WSWin,
                team_R=row.team_R,
                team_AB=row.team_AB,
                team_H=row.team_H,
                team_2B=row.team_2B,
                team_3B=row.team_3B,
                team_HR=row.team_HR,
                team_BB=row.team_BB,
                team_SO=row.team_SO,
                team_SB=row.team_SB,
                team_CS=row.team_CS,
                team_HBP=row.team_HBP,
                team_SF=row.team_SF,
                team_RA=row.team_RA,
                team_ER=row.team_ER,
                team_ERA=row.team_ERA,
                team_CG=row.team_CG,
                team_SHO=row.team_SHO,
                team_SV=row.team_SV,
                team_IPouts=row.team_IPouts,
                team_HA=row.team_HA,
                team_HRA=row.team_HRA,
                team_BBA=row.team_BBA,
                team_SOA=row.team_SOA,
                team_E=row.team_E,
                team_DP=row.team_DP,
                team_FP=row.team_FP,
                park_name=row.park_name,
                team_attendance=row.team_attendance,
                team_BPF=row.team_BPF,
                team_PPF=row.team_PPF,
                team_projW=row.team_projW,
                team_projL=row.team_projL,
            )
            .first()
        )

        # Alert that test failed, and for what row
        if not row_exists:
            print(
                f"Row could not be found for: teamID={row.teamID}, yearID={row.yearID}, lgID={row.lgID}"
            )
            rows_match = False

    # Commit and close sessions
    sq_session.commit()
    sq_session.close()
    bb_session.commit()
    bb_session.close()

    # Output test result
    if not rows_match:
        return "FAILURE: teams"
    else:
        return ""


def compare_existing_schools_entries():

    # Create sessions
    sq_session = create_session_from_str(create_enginestr_from_values(cfg.mysql))
    bb_session = create_session_from_str(
        create_enginestr_from_values(cfg.baseballmysql)
    )

    # Get the original Schools rows
    bb_result = bb_session.query(Schools).all()

    # Go through each row in the original baseball database to make sure ours matches
    rows_match = True
    for row in bb_result:
        row_exists = (
            sq_session.query(Schools)
            .filter_by(
                schoolId=row.schoolId,
                school_name=row.school_name,
                school_city=row.school_city,
                school_state=row.school_state,
                school_country=row.school_country,
            )
            .first()
        )

        # Alert that test failed, and for what row
        if not row_exists:
            print(
                f"Row could not be found for: schoolId={row.schoolId}, school_name={row.school_name}"
            )
            rows_match = False

    # Commit and close sessions
    sq_session.commit()
    sq_session.close()
    bb_session.commit()
    bb_session.close()

    # Output test result
    if not rows_match:
        return "FAILURE: schools"
    else:
        return ""
