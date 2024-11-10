from sqlalchemy import (
    Column,
    Date,
    Double,
    ForeignKey,
    Index,
    Integer,
    SmallInteger,
    String,
)
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
    allstarfull_entries = relationship(
        "AllstarFull", foreign_keys="[AllstarFull.lgID]", back_populates="league"
    )
    teams_entries = relationship(
        "Teams", foreign_keys="[Teams.lgID]", back_populates="league"
    )
    league_seriespost_winner = relationship(
        "SeriesPost",
        foreign_keys="[SeriesPost.lgIDwinner]",
        back_populates="winner_league",
    )
    league_seriespost_loser = relationship(
        "SeriesPost",
        foreign_keys="[SeriesPost.lgIDloser]",
        back_populates="loser_league",
    )


class Teams(Base):
    __tablename__ = "teams"
    teams_ID = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    teamID = Column(String(3), nullable=False)
    yearID = Column(SmallInteger, nullable=False)
    lgID = Column(String(2), ForeignKey("leagues.lgID"), nullable=True)
    divID = Column(String(1), nullable=True)
    franchID = Column(String(3), nullable=True)
    team_name = Column(String(50), nullable=True)
    team_rank = Column(SmallInteger, nullable=True)
    team_G = Column(SmallInteger, nullable=True)
    team_G_home = Column(SmallInteger, nullable=True)
    team_W = Column(SmallInteger, nullable=True)
    team_L = Column(SmallInteger, nullable=True)
    DivWin = Column(String(1), nullable=True)
    WCWin = Column(String(1), nullable=True)
    LgWin = Column(String(1), nullable=True)
    WSWin = Column(String(1), nullable=True)
    team_R = Column(SmallInteger, nullable=True)
    team_AB = Column(SmallInteger, nullable=True)
    team_H = Column(SmallInteger, nullable=True)
    team_2B = Column(SmallInteger, nullable=True)
    team_3B = Column(SmallInteger, nullable=True)
    team_HR = Column(SmallInteger, nullable=True)
    team_BB = Column(SmallInteger, nullable=True)
    team_SO = Column(SmallInteger, nullable=True)
    team_SB = Column(SmallInteger, nullable=True)
    team_CS = Column(SmallInteger, nullable=True)
    team_HBP = Column(SmallInteger, nullable=True)
    team_SF = Column(SmallInteger, nullable=True)
    team_RA = Column(SmallInteger, nullable=True)
    team_ER = Column(SmallInteger, nullable=True)
    team_ERA = Column(Double, nullable=True)
    team_CG = Column(SmallInteger, nullable=True)
    team_SHO = Column(SmallInteger, nullable=True)
    team_SV = Column(SmallInteger, nullable=True)
    team_IPouts = Column(Integer, nullable=True)
    team_HA = Column(SmallInteger, nullable=True)
    team_HRA = Column(SmallInteger, nullable=True)
    team_BBA = Column(SmallInteger, nullable=True)
    team_SOA = Column(SmallInteger, nullable=True)
    team_E = Column(SmallInteger, nullable=True)
    team_DP = Column(SmallInteger, nullable=True)
    team_FP = Column(Double, nullable=True)
    park_name = Column(String(50), nullable=True)
    team_attendance = Column(Integer, nullable=True)
    team_BPF = Column(SmallInteger, nullable=True)
    team_PPF = Column(SmallInteger, nullable=True)
    team_projW = Column(SmallInteger, nullable=True)
    team_projL = Column(SmallInteger, nullable=True)

    # Define the MUL (Index) fields
    __table_args__ = (
        Index("idx_teamID", "teamID"),
        Index("idx_lgID", "lgID"),
        Index("idx_franchID", "franchID"),
    )

    # Define relationships
    league = relationship(
        "Leagues", foreign_keys=[lgID], back_populates="teams_entries"
    )
    seriespost_winner = relationship(
        "SeriesPost",
        foreign_keys="[SeriesPost.teamIDwinner]",
        back_populates="winner",
    )
    seriespost_loser = relationship(
        "SeriesPost",
        foreign_keys="[SeriesPost.teamIDloser]",
        back_populates="loser",
    )


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


class Schools(Base):
    __tablename__ = "schools"
    schoolId = Column(String(15), primary_key=True, nullable=False)
    school_name = Column(String(255), nullable=True)
    school_city = Column(String(55), nullable=True)
    school_state = Column(String(55), nullable=True)
    school_country = Column(String(55), nullable=True)


class SeriesPost(Base):
    __tablename__ = "seriespost"
    seriespost_ID = Column(Integer, primary_key=True, nullable=False)
    teamIDwinner = Column(String(3), ForeignKey("teams.teamID"), nullable=False)
    lgIDwinner = Column(String(3), ForeignKey("leagues.lgID"), nullable=False)
    teamIDloser = Column(String(3), ForeignKey("teams.teamID"), nullable=False)
    lgIDloser = Column(String(3), ForeignKey("leagues.lgID"), nullable=False)
    yearID = Column(SmallInteger, nullable=False)
    round = Column(String(5), nullable=False)
    wins = Column(SmallInteger, nullable=True)
    losses = Column(SmallInteger, nullable=True)
    ties = Column(SmallInteger, nullable=True)

    winner = relationship(
        "Teams", foreign_keys=[teamIDwinner], back_populates="seriespost_winner"
    )
    loser = relationship(
        "Teams", foreign_keys=[teamIDloser], back_populates="seriespost_loser"
    )
    winner_league = relationship(
        "Leagues", foreign_keys=[lgIDwinner], back_populates="league_seriespost_winner"
    )
    loser_league = relationship(
        "Leagues", foreign_keys=[lgIDloser], back_populates="league_seriespost_loser"
    )


class Pitching(Base):
    __tablename__ = "pitching"
    pitchingID = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    playerID = Column(String(9), ForeignKey("people.playerID"), nullable=False)
    yearID = Column(SmallInteger, nullable=False)
    teamID = Column(String(3), ForeignKey("teams.teamID"), nullable=False)
    stint = Column(SmallInteger, nullable=False)
    p_W = Column(SmallInteger, nullable=True)
    p_L = Column(SmallInteger, nullable=True)
    p_G = Column(SmallInteger, nullable=True)
    p_GS = Column(SmallInteger, nullable=True)
    p_CG = Column(SmallInteger, nullable=True)
    p_SHO =Column(SmallInteger, nullable=True)
    p_SV = Column(SmallInteger, nullable=True)
    p_IPOuts = Column(Integer, nullable=True)
    p_H = Column(SmallInteger, nullable=True)
    p_ER = Column(SmallInteger, nullable=True)
    p_ER = Column(SmallInteger, nullable=True)
    p_BB = Column(SmallInteger, nullable=True)
    p_SO = Column(SmallInteger, nullable=True)
    p_BAOpp = Column(Double, nullable=True)
    p_ERA = Column(Double, nullable=True)
    p_IBB = Column(SmallInteger, nullable=True)
    p_WP = Column(SmallInteger, nullable=True)
    p_HBP = Column(SmallInteger, nullable=True)
    p_BK = Column(SmallInteger, nullable=True)
    p_BFP = Column(SmallInteger, nullable=True)
    p_GF = Column(SmallInteger, nullable=True)
    p_R = Column(SmallInteger, nullable=True)
    p_SH = Column(SmallInteger, nullable=True)
    p_SF = Column(SmallInteger, nullable=True)
    p_GIDP = Column(SmallInteger, nullable=True)

class Appearances(Base):
    __tablename__ = "appearances"
    appearances_ID = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    playerID = Column(String(9), ForeignKey("people.playerID"), nullable=False)
    yearID = Column(SmallInteger, nullable=False)
    teamID = Column(String(3), ForeignKey("teams.teamID"), nullable=False)
    G_all = Column(SmallInteger, nullable=True)
    GS = Column(SmallInteger, nullable=True)
    G_batting = Column(SmallInteger, nullable=True)
    G_defense = Column(SmallInteger, nullable=True)
    G_p = Column(SmallInteger, nullable=True)
    G_c = Column(SmallInteger, nullable=True)
    G_1b = Column(SmallInteger, nullable=True)
    G_2b = Column(SmallInteger, nullable=True)
    G_3b = Column(SmallInteger, nullable=True)
    G_ss = Column(SmallInteger, nullable=True)
    G_lf = Column(SmallInteger, nullable=True)
    G_cf = Column(SmallInteger, nullable=True)
    G_rf = Column(SmallInteger, nullable=True)
    G_of = Column(SmallInteger, nullable=True)
    G_dh = Column(SmallInteger, nullable=True)
    G_ph = Column(SmallInteger, nullable=True)
    G_pr = Column(SmallInteger, nullable=True)

class Fielding(Base):
    __tablename__ = "fielding"
    fielding_ID = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
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
