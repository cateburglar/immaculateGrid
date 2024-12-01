from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import app.csi3335f2024 as cfg
from app.models import AllstarFull


def get_all_entries_allstarfull():
    # Create engine
    enginestr = (
        "mysql+pymysql://"
        + cfg.mysql["user"]
        + ":"
        + cfg.mysql["password"]
        + "@"
        + cfg.mysql["host"]
        + "/"
        + cfg.mysql["db"]
    )
    engine = create_engine(enginestr)
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        # Query all entries in AllstarFull
        all_entries = session.query(AllstarFull).all()
        return all_entries
    finally:
        session.close()
