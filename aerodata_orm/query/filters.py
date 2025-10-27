"""
Filter operators for query building.
"""

from enum import Enum


class FilterOperator(str, Enum):
    """Filter operators for queries."""
    
    EQ = "eq"  # Equal
    NE = "ne"  # Not equal
    GT = "gt"  # Greater than
    GTE = "gte"  # Greater than or equal
    LT = "lt"  # Less than
    LTE = "lte"  # Less than or equal
    CONTAINS = "contains"  # Contains substring
    IN = "in"  # In list
    NOT_IN = "not_in"  # Not in list
    IS_NULL = "is_null"  # Is null
    IS_NOT_NULL = "is_not_null"  # Is not null


class Aggregation:
    """Aggregation functions for queries."""
    
    @staticmethod
    def avg(field: str) -> dict:
        """Average aggregation."""
        return {"type": "avg", "field": field}
    
    @staticmethod
    def sum(field: str) -> dict:
        """Sum aggregation."""
        return {"type": "sum", "field": field}
    
    @staticmethod
    def min(field: str) -> dict:
        """Minimum aggregation."""
        return {"type": "min", "field": field}
    
    @staticmethod
    def max(field: str) -> dict:
        """Maximum aggregation."""
        return {"type": "max", "field": field}
    
    @staticmethod
    def count(field: str = "*") -> dict:
        """Count aggregation."""
        return {"type": "count", "field": field}
