from sqlalchemy import Column, ForeignKey, Integer, SmallInteger, String
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class AllstarFull(Base):
    __tablename__ = "allstarfull"
    allstarfull_ID = Column(Integer, primary_key=True, nullable=False)
    playerID = Column(String(9), ForeignKey("people.playerID"), nullable=False)
    lgID = Column(String(2), ForeignKey("leagues.lgID"), nullable=False)
    teamID = Column(String(3), nullable=False)
    yearID = Column(SmallInteger, nullable=False)
    gameID = Column(String(12))
    GP = Column(SmallInteger)
    startingPos = Column(SmallInteger)
