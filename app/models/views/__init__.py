from sqlalchemy import Column, Float, Integer, SmallInteger, String
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class LgAvgView(Base):
    __tablename__ = "lgavgview"

    yearID = Column(SmallInteger, primary_key=True)
    lgERA = Column(Float)
    lgHR = Column(Float)
    lgBB = Column(Float)
    lgHBP = Column(Float)
    lgK = Column(Float)
    lgIP = Column(Float)
