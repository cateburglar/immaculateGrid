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

class PitchingStatsView(Base):
    __tablename__ = "pitchingstatsview"

    # Basic player/team info
    playerID = Column(String(9), primary_key = True)
    teamID = Column(String(3), nullable = False)
    yearID = Column(SmallInteger, nullable = False)
    stint = Column(SmallInteger, nullable = False)
    nameFirst = Column(String(255), nullable = True)
    nameLast = Column(String(255), nullable = True)
    nameGiven = Column(String(255), nullable = True)
    age = Column(Integer, nullable = True)

    # Traditional pitching stats
    p_G = Column(SmallInteger, nullable = True)
    p_GS = Column(SmallInteger, nullable = True)

    # Advanced pitching metrics
    p_IP = Column(Float, nullable = True) # Derived from p_IPouts
    p_K_percent = Column(Float, nullable = True) # Strikeout Percentage
    p_BB_percent = Column(Float, nullable = True) # Walk Percentage
    p_HR_div9 = Column(Float, nullable = True) # HR per 9 innings
    p_BABIP = Column(Float, nullable = True) # Batting Average on Balls In Play
    p_LOB_percent = Column(Float, nullable = True) # Left On Base Percentage
    p_GB_percent= Column(Float, nullable = True) # Ground Ball Percentage
    p_HR_div_FB = Column(Float, nullable = True) # HR per Fly Ball
    p_ERA = Column(Float, nullable = True) # Earned Run Average
    p_FIP = Column(Float, nullable = True) # Fielding Independent Pitching
    p_XFIP = Column(Float, nullable = True) # Expected Fielding Independent Pitching
    p_WAR = Column(Float, nullable = True) # Wins Above Replacement

    # __table_args__ and relationships not needed because this is a view
