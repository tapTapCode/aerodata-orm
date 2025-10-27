"""
Query builder with fluent API for ORM operations.
"""

from typing import Any, Generic, List, Optional, Type, TypeVar, Dict
from .filters import FilterOperator

T = TypeVar("T")


class QueryBuilder(Generic[T]):
    """
    Fluent API query builder for ORM operations.
    
    Example:
        >>> Aircraft.query(backend) \\
        ...     .where(manufacturer="Boeing") \\
        ...     .where(max_speed__gt=500) \\
        ...     .with_engines() \\
        ...     .order_by("-max_speed") \\
        ...     .limit(10) \\
        ...     .all()
    """
    
    def __init__(self, model_class: Type[T], backend: Any):
        """
        Initialize query builder.
        
        Args:
            model_class: Model class to query
            backend: Database backend
        """
        self.model_class = model_class
        self.backend = backend
        self._filters: List[Dict[str, Any]] = []
        self._relations: List[str] = []
        self._order_by_fields: List[str] = []
        self._limit_value: Optional[int] = None
        self._offset_value: Optional[int] = None
    
    def where(self, **kwargs) -> "QueryBuilder[T]":
        """
        Add filter conditions.
        
        Supports Django-style lookups:
        - field=value: Exact match
        - field__gt=value: Greater than
        - field__gte=value: Greater than or equal
        - field__lt=value: Less than
        - field__lte=value: Less than or equal
        - field__contains=value: Contains substring
        - field__in=values: In list
        
        Args:
            **kwargs: Filter conditions
            
        Returns:
            Self for chaining
            
        Example:
            >>> .where(manufacturer="Boeing", max_speed__gt=500)
        """
        for key, value in kwargs.items():
            if "__" in key:
                field, operator = key.rsplit("__", 1)
                self._filters.append({
                    "field": field,
                    "operator": operator,
                    "value": value
                })
            else:
                # Exact match
                self._filters.append({
                    "field": key,
                    "operator": "eq",
                    "value": value
                })
        return self
    
    def with_relations(self, *relations: str) -> "QueryBuilder[T]":
        """
        Eager load relationships.
        
        Args:
            *relations: Relationship names to load
            
        Returns:
            Self for chaining
            
        Example:
            >>> .with_relations("engines", "materials")
        """
        self._relations.extend(relations)
        return self
    
    def with_engines(self) -> "QueryBuilder[T]":
        """Shortcut for loading engines relationship."""
        return self.with_relations("engines")
    
    def with_aircraft(self) -> "QueryBuilder[T]":
        """Shortcut for loading aircraft relationship."""
        return self.with_relations("aircraft")
    
    def with_route(self) -> "QueryBuilder[T]":
        """Shortcut for loading route relationship."""
        return self.with_relations("route")
    
    def order_by(self, *fields: str) -> "QueryBuilder[T]":
        """
        Order results by field(s).
        
        Prefix field name with '-' for descending order.
        
        Args:
            *fields: Field names (e.g., "max_speed", "-created_at")
            
        Returns:
            Self for chaining
            
        Example:
            >>> .order_by("-max_speed", "manufacturer")
        """
        self._order_by_fields.extend(fields)
        return self
    
    def limit(self, limit: int) -> "QueryBuilder[T]":
        """
        Limit number of results.
        
        Args:
            limit: Maximum number of results
            
        Returns:
            Self for chaining
        """
        self._limit_value = limit
        return self
    
    def offset(self, offset: int) -> "QueryBuilder[T]":
        """
        Skip first N results.
        
        Args:
            offset: Number of results to skip
            
        Returns:
            Self for chaining
        """
        self._offset_value = offset
        return self
    
    def first(self) -> Optional[T]:
        """
        Execute query and return first result.
        
        Returns:
            First model instance or None
        """
        self._limit_value = 1
        results = self.backend.execute_query(
            model_class=self.model_class,
            filters=self._filters,
            relations=self._relations,
            order_by=self._order_by_fields,
            limit=self._limit_value,
            offset=self._offset_value
        )
        return results[0] if results else None
    
    def all(self) -> List[T]:
        """
        Execute query and return all results.
        
        Returns:
            List of model instances
        """
        return self.backend.execute_query(
            model_class=self.model_class,
            filters=self._filters,
            relations=self._relations,
            order_by=self._order_by_fields,
            limit=self._limit_value,
            offset=self._offset_value
        )
    
    def count(self) -> int:
        """
        Count number of results without fetching them.
        
        Returns:
            Number of matching records
        """
        return self.backend.count_query(
            model_class=self.model_class,
            filters=self._filters
        )
    
    def exists(self) -> bool:
        """
        Check if any results exist.
        
        Returns:
            True if at least one result exists
        """
        return self.count() > 0
    
    def group_by(self, *fields: str) -> "QueryBuilder[T]":
        """
        Group results by field(s).
        
        Args:
            *fields: Field names to group by
            
        Returns:
            Self for chaining
        """
        # This would be implemented by backend
        raise NotImplementedError("Group by requires backend implementation")
    
    def aggregate(self, aggregation: Any) -> "QueryBuilder[T]":
        """
        Add aggregation (avg, sum, min, max, count).
        
        Args:
            aggregation: Aggregation function
            
        Returns:
            Self for chaining
        """
        # This would be implemented by backend
        raise NotImplementedError("Aggregation requires backend implementation")
