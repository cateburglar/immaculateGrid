from .query_filter import QueryFilter


class PositionFilter(QueryFilter):
    """
    Filter for applying position related conditions to the query
    """

    def __init__(self, query, position=None, yearid=None):
        super().__init__(query)
        self.position = position
        self.year = yearid

    def apply(self):
        """
        Apply the position filter to the query
        """

        if self.position:
            self.query = self.query.filter_by(position=self.position)

        if self.year:
            self.query = self.query.filter_by(yearid=self.year)
