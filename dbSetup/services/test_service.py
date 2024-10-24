import csi3335f2024 as cfg
from models import AllstarFull, Leagues, People
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def compare_existing_allstarfull_entries():

    # Create engine
    sqenginestr = (
        "mysql+pymysql://"
        + cfg.mysql["user"]
        + ":"
        + cfg.mysql["password"]
        + "@"
        + cfg.mysql["host"]
        + "/"
        + cfg.mysql["db"]
    )
    sq_engine = create_engine(sqenginestr)
    sq_Session = sessionmaker(bind=sq_engine)
    sq_session = sq_Session()

    bbenginestr = (
        "mysql+pymysql://"
        + cfg.baseballmysql["user"]
        + ":"
        + cfg.baseballmysql["password"]
        + "@"
        + cfg.baseballmysql["host"]
        + "/"
        + cfg.baseballmysql["db"]
    )

    bb_engine = create_engine(bbenginestr)
    bb_Session = sessionmaker(bind=bb_engine)
    bb_session = bb_Session()

    bb_result = bb_session.query(AllstarFull).all()

    # Go through each row in the original baseball database to make sure they match
    rows_match = True
    for row in bb_result:
        row_exists = sq_session.query(AllstarFull).filter_by(
            playerID=row.playerID,
            yearID=row.yearID,
            lgID=row.lgID,
            teamID=row.teamID,
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
