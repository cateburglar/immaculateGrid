from abc import ABC, abstractmethod

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
        self.query = self.query.join(
            appearances_alias, People.playerID == appearances_alias.playerID
        ).filter(appearances_alias.teamID == self.team)
        return self.query


class CareerStatFilter(QueryFilter):
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
        awards_alias = aliased(Awards, name=f"awards_{self.alias_suffix}")

        if self.category == "all_star":
            self.query = self.query.filter(People.all_star == True)
        elif self.category == "born_outside_us":
            self.query = self.query.filter(People.birthCountry != "USA")
        elif self.category == "cy_young":
            self.query = self.query.join(
                awards_alias, People.playerID == awards_alias.playerID
            ).filter(awards_alias.awardID == "Cy Young Award")
        elif self.category == "first_round_draft_pick":
            self.query = self.query.filter(People.first_round_draft_pick == True)
        elif self.category == "gold_glove":
            self.query = self.query.filter(People.gold_glove == True)
        elif self.category == "hall_of_fame":
            self.query = self.query.filter(People.hall_of_fame == True)
        elif self.category == "mvp":
            self.query = self.query.filter(People.mvp == True)
        elif self.category == "only_one_team":
            self.query = self.query.filter(People.only_one_team == True)
        elif self.category == "rookie_of_the_year":
            self.query = self.query.filter(People.rookie_of_the_year == True)
        elif self.category == "silver_slugger":
            self.query = self.query.filter(People.silver_slugger == True)
        elif self.category == "threw_a_no_hitter":
            self.query = self.query.filter(People.threw_a_no_hitter == True)
        elif self.category == "world_series_champ":
            self.query = self.query.filter(People.world_series_champ == True)

        if self.team:
            appearances_alias = aliased(
                Appearances, name=f"appearances_{self.alias_suffix}"
            )

            # Filter by players who played on the team and got the award in that season
            self.query = (
                self.query.join(
                    appearances_alias, People.playerID == appearances_alias.playerID
                )
                .filter(appearances_alias.teamID == self.team)
                .filter(appearances_alias.yearID == awards_alias.yearID)
            )

        return self.query
