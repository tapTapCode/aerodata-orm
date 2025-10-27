"""
AeroData ORM - Python ORM-style library for aerospace engineering data models.
"""

from .models import Aircraft, Engine, Material, FlightData, BaseModel
from .backends import SQLAlchemyBackend, Neo4jBackend
from .query import QueryBuilder, FilterOperator, Aggregation

__version__ = "0.1.0"

__all__ = [
    # Models
    "Aircraft",
    "Engine",
    "Material",
    "FlightData",
    "BaseModel",
    # Backends
    "SQLAlchemyBackend",
    "Neo4jBackend",
    # Query
    "QueryBuilder",
    "FilterOperator",
    "Aggregation",
]
