from sqlalchemy import Column, Date, ForeignKey, Index, Integer, SmallInteger, String
from sqlalchemy.orm import DeclarativeBase, Mapped, relationship


class Base(DeclarativeBase):
    pass


class People(Base):
    __tablename__ = "people"
    playerID = Column(String(9), primary_key=True, nullable=False)
    birthYear = Column(Integer, nullable=True)
    birthMonth = Column(Integer, nullable=True)
    birthDay = Column(Integer, nullable=True)
    birthCountry = Column(String(255), nullable=True)
    birthState = Column(String(255), nullable=True)
    birthCity = Column(String(255), nullable=True)
    deathYear = Column(Integer, nullable=True)
    deathMonth = Column(Integer, nullable=True)
    deathDay = Column(Integer, nullable=True)
    deathCountry = Column(String(255), nullable=True)
    deathState = Column(String(255), nullable=True)
    deathCity = Column(String(255), nullable=True)
    nameFirst = Column(String(255), nullable=True)
    nameLast = Column(String(255), nullable=True)
    nameGiven = Column(String(255), nullable=True)
    weight = Column(Integer, nullable=True)
    height = Column(Integer, nullable=True)
    bats = Column(String(255), nullable=True)
    throws = Column(String(255), nullable=True)
    debutDate = Column(Date, nullable=True)
    finalGameDate = Column(Date, nullable=True)

    __table_args__ = (Index("idx_nameLast", "nameLast"),)  # nameLast is MUL in the db

    # Define relationship
    allstarfull_entries = relationship("AllstarFull", back_populates="player")


class Leagues(Base):
    __tablename__ = "leagues"
    lgID = Column(String(2), primary_key=True, nullable=False)
    league_name = Column(String(50), nullable=False)
    league_active = Column(String(1), nullable=False)

    # Define relationship
    allstarfull_entries = relationship("AllstarFull", back_populates="league")


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

    # Define relationships
    league = relationship("Leagues", back_populates="allstarfull_entries")
    player = relationship("People", back_populates="allstarfull_entries")
