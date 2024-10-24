import csi3335f2024 as cfg
from models import AllstarFull
from utils import create_enginestr_from_values, create_session_from_str


def compare_existing_allstarfull_entries():

    # Create sessions
    sq_session = create_session_from_str(create_enginestr_from_values(cfg.mysql))

    bb_session = create_session_from_str(
        create_enginestr_from_values(cfg.baseballmysql)
    )

    bb_result = bb_session.query(AllstarFull).all()

    # Go through each row in the original baseball database to make sure they match
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
