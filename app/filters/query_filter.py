from abc import ABC, abstractmethod

from sqlalchemy import cast, func
from sqlalchemy.orm import Query, aliased

from ..models import *


class QueryFilter(ABC):
    """
    Base class for all query filters. This class provides common functionality
    for applying filters to SQLAlchemy queries.
    """

    def __init__(self, query: Query, alias_suffix: int = 0):
        """
        Initialize the filter with a given query.

        :param query: The SQLAlchemy query object to apply filters to.
        """
        self.query = query
        self.alias_suffix = alias_suffix

    @abstractmethod
    def apply(self):
        """
        Apply the filter to the query. This method must be overridden by subclasses.
        """
        pass


class TeamFilter(QueryFilter):
    def __init__(
        self,
        query: Query,
        team: str,
        alias_suffix: int = 0,
    ):
        super().__init__(query, alias_suffix)
        self.team = team

    def apply(self):
        appearances_alias = aliased(
            Appearances, name=f"appearances_{self.alias_suffix}"
        )

        # Create a subquery to get the teamIDs that match the team name
        team_subquery = (
            self.query.session.query(Teams.teamID)
            .filter(Teams.team_name == self.team)
            .subquery()
        )

        self.query = self.query.join(
            appearances_alias, People.playerID == appearances_alias.playerID
        ).filter(appearances_alias.teamID.in_(team_subquery))
        return self.query


class CareerStatFilter(QueryFilter):
    def __init__(
        self,
        query: Query,
        stat: str,
        value: float,
        team: str = None,
        alias_suffix: int = 0,
    ):
        super().__init__(query, alias_suffix)
        self.stat = stat
        self.value = value
        self.team = team

    def apply(self):
        # Create aliases for joins
        appearances_alias = aliased(
            Appearances, name=f"appearances_{self.alias_suffix}"
        )

        if self.stat == "avg_career":
            # Query to calculate career AVG
            self.query = (
                self.query(
                    Batting.playerID,
                    func.sum(Batting.b_H).label("career_hits"),
                    func.sum(Batting.b_AB).label("career_at_bats"),
                    (cast(func.sum(Batting.b_H), Float) / func.sum(Batting.b_AB)).label(
                        "career_avg"
                    ),
                )
                .group_by(Batting.playerID)
                .having(
                    (cast(func.sum(Batting.b_H), Float) / func.sum(Batting.b_AB))
                    >= self.value
                )
            )

        if self.operator == "greater_than":
            self.query = self.query.filter(getattr(People, self.stat) >= self.value)
        elif self.operator == "less_than":
            self.query = self.query.filter(getattr(People, self.stat) <= self.value)

        # Filter by players who played on that team at least once
        if self.team:
            # Create a subquery to get the teamIDs that match the team name
            team_subquery = (
                self.query.session.query(Teams.teamID)
                .filter(Teams.team_name == self.team)
                .subquery()
            )

            # Join People and Appearances then filter by players who have at least one appearance
            # with the team in question
            self.query = self.query.join(
                appearances_alias,
                People.playerID == appearances_alias.playerID,
            ).filter(appearances_alias.teamID.in_(team_subquery))

        return self.query


class SeasonStatFilter(QueryFilter):
    def __init__(
        self,
        query: Query,
        stat: str,
        operator: str,
        value: float,
        team: str = None,
        alias_suffix: int = 0,
    ):
        super().__init__(query, alias_suffix)
        self.stat = stat
        self.operator = operator
        self.value = value
        self.team = team

    def apply(self):
        if self.team:
            self.query = self.query.join(
                Appearances, People.playerID == Appearances.playerID
            ).filter(Appearances.teamID == self.team)

        if self.operator == "greater_than":
            self.query = self.query.filter(getattr(People, self.stat) >= self.value)
        elif self.operator == "less_than":
            self.query = self.query.filter(getattr(People, self.stat) <= self.value)

        return self.query


class PositionFilter(QueryFilter):
    def __init__(
        self,
        query: Query,
        position: str,
        team: str = None,
        alias_suffix: int = 0,
    ):
        super().__init__(query, alias_suffix)
        self.position = position
        self.team = team

    def apply(self):
        # Filter for pitching
        if self.position == "pitched":
            self.query = self.query.join(Pitching, People.playerID == Pitching.playerID)
            if self.team:
                self.query = self.query.filter(Pitching.teamID == self.team)

        if self.team:
            self.query = self.query.filter_by(teamID=self.team)

        return self.query


class MiscFilter(QueryFilter):
    def __init__(
        self,
        query: Query,
        category: str,
        team: str = None,
        alias_suffix: int = 0,
    ):
        super().__init__(query, alias_suffix)
        self.category = category
        self.team = team

    def apply(self):
        # Create aliases to join tables
        awards_alias = aliased(Awards, name=f"awards_{self.alias_suffix}")
        allstarfull_alias = aliased(
            AllstarFull, name=f"allstarfull_{self.alias_suffix}"
        )
        appearances_alias = aliased(
            Appearances, name=f"appearances_{self.alias_suffix}"
        )
        seriespost_alias = aliased(SeriesPost, name=f"seriespost_{self.alias_suffix}")
        draft_alias = aliased(Draft, name=f"draft_{self.alias_suffix}")
        nohitters_alias = aliased(NoHitters, name=f"nohitters_{self.alias_suffix}")

        # Finds all stars by joining with allstarfull
        if self.category == "All Star":
            self.query = self.query.join(
                allstarfull_alias, People.playerID == allstarfull_alias.playerID
            )

        # Finds players born outside the US by checking the birthCountry
        elif self.category == "Born Outside US":
            self.query = self.query.filter(People.birthCountry != "USA")

        # Finds first round picks by joining with the draft table
        elif self.category == "First Round Draft Pick":
            self.query = self.query.join(
                draft_alias, People.playerID == draft_alias.playerID
            )
        elif self.category == "Hall of Fame":
            self.query = self.query.filter(People.hall_of_fame == True)

        # Finds players who only played on one team by joining with appearances and
        # filtering to players who only appeared with one team
        elif self.category == "Only One Team":
            # Get players who have only played for one team
            subquery = (
                self.query.session.query(Appearances.playerID)
                .group_by(Appearances.playerID)
                .having(func.count(func.distinct(Appearances.teamID)) == 1)
                .subquery()
            )

            # Join the People to the matching players
            self.query = self.query.join(
                subquery, People.playerID == subquery.c.playerID
            )

        # Finds players who have thrown no-hitters by joining with the no-hitters table
        elif self.category == "No Hitter":
            self.query = self.query.join(
                nohitters_alias, People.playerID == nohitters_alias.playerID
            )

        # Gets the players who are in the NLHOF
        elif self.category == "Negro Leagues":
            self.query = self.query.filter(People.nl_hof == True)

        # Finds WS Champs by joining appearances and seriespost to find players who played on
        # winning teams
        elif self.category == "WS Champ":
            appearances_ws_alias = aliased(
                Appearances, name=f"appearances_ws_{self.alias_suffix}"
            )
            self.query = (
                self.query.join(
                    appearances_ws_alias,
                    People.playerID == appearances_ws_alias.playerID,
                )
                .join(
                    seriespost_alias,
                    (appearances_ws_alias.teamID == seriespost_alias.teamIDwinner)
                    & (appearances_ws_alias.yearID == seriespost_alias.yearID),
                )
                .filter(seriespost_alias.round == "WS")
            )

        # Finds standard awards by joining with the awards table and filtering
        # by awards rows with the category
        else:  # Standard awards
            self.query = self.query.join(
                awards_alias, People.playerID == awards_alias.playerID
            ).filter(awards_alias.awardID == self.category)

        # If a team is provided, ensure rows match that team
        if self.team:
            # Create a subquery to get the teamIDs that match the team name
            team_subquery = (
                self.query.session.query(Teams.teamID)
                .filter(Teams.team_name == self.team)
                .subquery()
            )

            # Since appearances isn't used to find all stars this has to be done
            # separately
            if self.category == "All Star":
                self.query = self.query.filter(
                    allstarfull_alias.teamID.in_(team_subquery)
                )

            else:
                # Filter by players who played on the team in that season
                self.query = (
                    self.query.join(
                        appearances_alias,
                        People.playerID == appearances_alias.playerID,
                    )
                    .filter(appearances_alias.teamID.in_(team_subquery))
                    .filter(appearances_alias.yearID == awards_alias.yearID)
                )

        return self.query
