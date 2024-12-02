from sqlalchemy import (
    Column,
    Float,
    Integer,
    SmallInteger,
    String,
)
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class BattingStatsView(Base):
    __tablename__ = "battingstatsview"

    player_id = Column(String, primary_key=True)
    year_id = Column(SmallInteger, primary_key=True)
    team_id = Column(String, primary_key=True)
    stint = Column(SmallInteger, primary_key=True)
    position = Column(String)
    pa = Column(Integer)  # Plate Appearances
    pt_1b = Column(Float)  # Playing Time at 1B
    pt_2b = Column(Float)  # Playing Time at 2B
    pt_3b = Column(Float)  # Playing Time at 3B
    pt_ss = Column(Float)  # Playing Time at SS
    pt_lf = Column(Float)  # Playing Time at LF
    pt_cf = Column(Float)  # Playing Time at CF
    pt_rf = Column(Float)  # Playing Time at RF
    pt_dh = Column(Float)  # Playing Time at DH
    woba = Column(Float)  # Weighted On-Base Average (wOBA)
