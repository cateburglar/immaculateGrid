from abc import ABC, abstractmethod

from sqlalchemy.orm import Query, aliased

from ..models import Appearances, People, Pitching
from ..static.constants import APPEARANCES_MAPPING

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
        alias_suffix: int = 1,
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
        alias_suffix: int = 2,
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
        alias_suffix: int = 3,
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


"""
PositionFilter applies a filter to the query to include players who have 
played a specific position in a given team. If a team is provided, 
the filter also ensures that the player was associated with that team during 
the relevant seasons.

Attributes:
    position (str): The position abbreviation (e.g., "P" for pitcher, "C" for catcher).
    team (str, optional): The team ID to filter players by. Defaults to None (no team filter).
    
Methods:
    apply(): Applies the position filter to the query and returns the updated query.

Returns:
    query: The SQLAlchemy query object with the position filter applied.
"""
class PositionFilter(QueryFilter):

    def __init__(
        self,
        query: Query,
        position: str,
        team: str = None,
        alias_suffix: int = 4,
    ):
        
        """
        Initializes the filter with a given query, position, team, and alias suffix.
        
        :param query: SQLAlchemy query object to apply the filter to.
        :param position: The position abbreviation to filter by (e.g., "P" for Pitched).
        :param team: Optional team ID to filter by.
        :param alias_suffix: Optional suffix for table aliasing.
        """
        super().__init__(query, alias_suffix)
        self.position = position
        self.team = team

    def apply(self):
        """
        Applies the position filter to the query using the appropriate field from
        the APPEARANCES table based on the position abbreviation (e.g., "P" for pitcher).
        
        :return: The modified query with the applied filter.
        """
        
        # Get the corresponding field from the APPEARANCES table for the position
        position_field = APPEARANCES_MAPPING[self.position]

        # Alias the Appearances table for the query
        # so that we can join the appearances table multiple times if needed
        appearances_alias = aliased(Appearances, name=f"appearances_{self.alias_suffix}")
        self.alias_suffix += 1

        # Join the Appearances table with People and filter by the position field
        self.query = self.query.join(appearances_alias, People.playerID == appearances_alias.playerID)

        # Filter based on the number of games played for the position (should be greater than 0)
        self.query = self.query.filter(getattr(appearances_alias, position_field) > 0)

        # If a team is provided, filter by team ID
        if self.team:
            self.query = self.query.filter(appearances_alias.teamID == self.team)

        return self.query


class MiscFilter(QueryFilter):
    def __init__(
        self,
        query: Query,
        category: str,
        team: str = None,
        alias_suffix: int = 5,
    ):
        super().__init__(query, alias_suffix)
        self.category = category
        self.team = team

    def apply(self):
        if self.team:
            self.query = self.query.join(
                Appearances, People.playerID == Appearances.playerID
            ).filter(Appearances.teamID == self.team)

        if self.category == "all_star":
            self.query = self.query.filter(People.all_star == True)
        elif self.category == "born_outside_us":
            self.query = self.query.filter(People.birthCountry != "USA")
        elif self.category == "cy_young":
            self.query = self.query.filter(People.cy_young == True)
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

        return self.query
