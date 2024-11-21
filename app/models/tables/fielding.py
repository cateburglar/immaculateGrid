from sqlalchemy import Column, ForeignKey, Integer, SmallInteger, String, Index
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass

class Fielding(Base):
    __tablename__ = "fielding"
    fielding_ID = Column(Integer, primary_key=True, nullable=False)
    playerID = Column(String(9), ForeignKey("people.playerID"), nullable=False)
    yearID = Column(SmallInteger, nullable=False)
    teamID = Column(String(3), ForeignKey("teams.teamID"), nullable=False)
    stint = Column(SmallInteger, nullable=False)
    position = Column(String(2), nullable=True)
    f_G = Column(SmallInteger, nullable=True)
    f_GS = Column(SmallInteger, nullable=True)
    f_InnOuts = Column(SmallInteger, nullable=True)
    f_PO = Column(SmallInteger, nullable=True)
    f_A = Column(SmallInteger, nullable=True)
    f_E = Column(SmallInteger, nullable=True)
    f_DP = Column(SmallInteger, nullable=True)
    f_PB = Column(SmallInteger, nullable=True)
    f_WP = Column(SmallInteger, nullable=True)
    f_SB = Column(SmallInteger, nullable=True)
    f_CS = Column(SmallInteger, nullable=True)
    f_ZR = Column(SmallInteger, nullable=True)

    # Define the MUL (Index) fields
    #this speeds up data retrieval by these columns
    __table_args__ = (
        Index("idx_teamID", "teamID"),
        Index("idx_playerID_yearID_teamID", "playerID", "yearID", "teamID"),
    )
