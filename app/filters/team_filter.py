from .query_filter import QueryFilter


class TeamFilter(QueryFilter):
    """
    Filter for applying team related conditions to the query.
    """

    def __init__(self, query, team_name=None, yearid=None):
        super().__init__(query)
        self.team_name = team_name
        self.year = yearid

    def apply(self):
        """
        Apply the team name filter to the query.
        """
        if self.team_name:
            self.query = self.query.filter_by(team_name=self.team_name)

        if self.year:
            self.query = self.query.filter_by(yearid=self.year)

        return self.query
