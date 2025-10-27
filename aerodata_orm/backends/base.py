"""
Base backend interface for database operations.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Type


class Backend(ABC):
    """
    Abstract base class for database backends.
    Defines interface that all backends must implement.
    """
    
    @abstractmethod
    def connect(self) -> None:
        """Establish connection to database."""
        pass
    
    @abstractmethod
    def disconnect(self) -> None:
        """Close database connection."""
        pass
    
    @abstractmethod
    def execute_query(
        self,
        model_class: Type,
        filters: List[Dict[str, Any]],
        relations: List[str],
        order_by: List[str],
        limit: Optional[int],
        offset: Optional[int]
    ) -> List[Any]:
        """
        Execute a query and return results.
        
        Args:
            model_class: Model class to query
            filters: List of filter conditions
            relations: Relations to eager load
            order_by: Fields to order by
            limit: Maximum number of results
            offset: Number of results to skip
            
        Returns:
            List of model instances
        """
        pass
    
    @abstractmethod
    def count_query(
        self,
        model_class: Type,
        filters: List[Dict[str, Any]]
    ) -> int:
        """
        Count number of matching records.
        
        Args:
            model_class: Model class to query
            filters: List of filter conditions
            
        Returns:
            Number of matching records
        """
        pass
    
    @abstractmethod
    def get_by_id(self, model_class: Type, id: int) -> Optional[Any]:
        """
        Get a single record by ID.
        
        Args:
            model_class: Model class
            id: Primary key
            
        Returns:
            Model instance or None
        """
        pass
    
    @abstractmethod
    def insert(self, instance: Any) -> None:
        """
        Insert a new record.
        
        Args:
            instance: Model instance to insert
        """
        pass
    
    @abstractmethod
    def update(self, instance: Any) -> None:
        """
        Update an existing record.
        
        Args:
            instance: Model instance to update
        """
        pass
    
    @abstractmethod
    def delete(self, model_class: Type, id: int) -> None:
        """
        Delete a record by ID.
        
        Args:
            model_class: Model class
            id: Primary key
        """
        pass
