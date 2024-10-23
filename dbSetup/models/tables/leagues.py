from sqlalchemy import Column, String
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class Leagues(Base):
    __tablename__ = "leagues"
    lgID = Column(String(2), primary_key=True, nullable=False)
    league_name = Column(String(50), nullable=False)
    league_active = Column(String(1), nullable=False)
