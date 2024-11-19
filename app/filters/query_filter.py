from abc import ABC, abstractmethod

from sqlalchemy.orm import Query


class QueryFilter(ABC):
    """
    Base class for all query filters. This class provides common functionality
    for applying filters to SQLAlchemy queries.
    """

    def __init__(self, query: Query):
        """
        Initialize the filter with a given query.

        :param query: The SQLAlchemy query object to apply filters to.
        """
        self.query = query

    @abstractmethod
    def apply(self):
        """
        Apply the filter to the query. This method must be overridden by subclasses.
        """
        pass
