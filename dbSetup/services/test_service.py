import csi3335f2024 as cfg
from models import AllstarFull, People
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
        row_exists = sq_session.query(People).filter_by(
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
        return "FAILURE: people"
    else:
        return ""
