from sqlalchemy import Column, ForeignKey, Integer, SmallInteger, Decimal, String, Double
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class battingStatsView(Base):
    __tablename__ = "battingStatsView"
    Name = Column(String(511))
    Age = Column(SmallInteger)
    G = Column(SmallInteger)
    PA = Column(Integer)
    HR = Column(SmallInteger)
    SB = Column(SmallInteger)
    BB_percent = Column(Decimal(12, 4)) 
    K_percent = Column(Decimal(12, 4))  
    BABIP = Column(Decimal(10, 4)) 
    AVG = Column(Decimal(9, 4)) 
    SLG = Column(Decimal(15, 4)) 
    ISO = Column(Decimal(16, 4)) 
    b_1B = Column(Integer) 
    wOBA = Column(Decimal(19, 6))  
    wRCplus = Column(Decimal(43, 14)) 
    BsR = Column(Decimal(8, 1))  
    Total_Defensive_Plays = Column(Integer)
    FRAA = Column(Double)  
    WAR = Column(Double)  
    yearID = Column(SmallInteger, nullable=False)
    teamID = Column(String(3), nullable=False)