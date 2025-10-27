"""
Base model with ORM capabilities for all aerospace data models.
"""

from typing import Any, Dict, List, Optional, Type, TypeVar
from pydantic import BaseModel as PydanticBaseModel, ConfigDict
from datetime import datetime

T = TypeVar("T", bound="BaseModel")


class BaseModel(PydanticBaseModel):
    """
    Base class for all ORM models.
    Provides query methods, serialization, and database operations.
    """
    
    model_config = ConfigDict(
        validate_assignment=True,
        arbitrary_types_allowed=True,
        from_attributes=True,
    )
    
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    @classmethod
    def query(cls: Type[T], backend: Any) -> "QueryBuilder[T]":
        """
        Start a query using the fluent API.
        
        Args:
            backend: Database backend (SQLAlchemy, Neo4j, DynamoDB)
            
        Returns:
            QueryBuilder instance for chaining
            
        Example:
            >>> Aircraft.query(backend).where(manufacturer="Boeing").all()
        """
        from aerodata_orm.query.builder import QueryBuilder
        return QueryBuilder(cls, backend)
    
    def save(self, backend: Any) -> None:
        """
        Save the model to the database.
        
        Args:
            backend: Database backend
            
        Example:
            >>> aircraft = Aircraft(model="737-800", manufacturer="Boeing")
            >>> aircraft.save(backend)
        """
        if self.id is None:
            # Insert
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            backend.insert(self)
        else:
            # Update
            self.updated_at = datetime.now()
            backend.update(self)
    
    def delete(self, backend: Any) -> None:
        """
        Delete the model from the database.
        
        Args:
            backend: Database backend
        """
        if self.id is not None:
            backend.delete(self.__class__, self.id)
    
    @classmethod
    def get_by_id(cls: Type[T], backend: Any, id: int) -> Optional[T]:
        """
        Get a model instance by ID.
        
        Args:
            backend: Database backend
            id: Primary key
            
        Returns:
            Model instance or None
        """
        return backend.get_by_id(cls, id)
    
    def to_dict(self, exclude_none: bool = False) -> Dict[str, Any]:
        """
        Convert model to dictionary.
        
        Args:
            exclude_none: Whether to exclude None values
            
        Returns:
            Dictionary representation
        """
        return self.model_dump(exclude_none=exclude_none)
    
    @classmethod
    def from_dict(cls: Type[T], data: Dict[str, Any]) -> T:
        """
        Create model instance from dictionary.
        
        Args:
            data: Dictionary with model fields
            
        Returns:
            Model instance
        """
        return cls(**data)
    
    def __repr__(self) -> str:
        """String representation of the model."""
        fields = ", ".join(f"{k}={v!r}" for k, v in self.to_dict(exclude_none=True).items())
        return f"{self.__class__.__name__}({fields})"
