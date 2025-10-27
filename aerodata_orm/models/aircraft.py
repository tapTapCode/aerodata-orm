"""
Aircraft model for aerospace data.
"""

from typing import List, Optional
from pydantic import Field, field_validator
from .base import BaseModel


class Aircraft(BaseModel):
    """
    Aircraft model with specifications and performance characteristics.
    """
    
    model: str = Field(..., description="Aircraft model designation (e.g., 737-800, A320)")
    manufacturer: str = Field(..., description="Aircraft manufacturer (e.g., Boeing, Airbus)")
    
    # Performance specs
    max_speed: float = Field(..., description="Maximum speed in knots", gt=0)
    cruise_speed: Optional[float] = Field(None, description="Cruise speed in knots", gt=0)
    max_altitude: float = Field(..., description="Maximum altitude in feet", gt=0)
    range: Optional[float] = Field(None, description="Maximum range in nautical miles", gt=0)
    
    # Physical specs
    wingspan: float = Field(..., description="Wingspan in feet", gt=0)
    length: float = Field(..., description="Length in feet", gt=0)
    height: Optional[float] = Field(None, description="Height in feet", gt=0)
    
    # Weight specs (all in pounds)
    mtow: float = Field(..., description="Maximum takeoff weight in pounds", gt=0)
    mlw: Optional[float] = Field(None, description="Maximum landing weight in pounds", gt=0)
    oew: Optional[float] = Field(None, description="Operating empty weight in pounds", gt=0)
    
    # Capacity
    passenger_capacity: Optional[int] = Field(None, description="Maximum passenger capacity", ge=0)
    cargo_capacity: Optional[float] = Field(None, description="Cargo capacity in cubic feet", ge=0)
    fuel_capacity: Optional[float] = Field(None, description="Fuel capacity in gallons", ge=0)
    
    # Engine info
    num_engines: Optional[int] = Field(None, description="Number of engines", ge=1, le=8)
    engine_type: Optional[str] = Field(None, description="Engine type (jet, turboprop, piston)")
    
    # Metadata
    first_flight: Optional[str] = Field(None, description="First flight date (YYYY-MM-DD)")
    production_status: Optional[str] = Field(None, description="Production status (active, retired)")
    
    # Relationships (loaded via query.with_engines(), etc.)
    engines: List["Engine"] = Field(default_factory=list, description="Associated engines")
    materials: List["Material"] = Field(default_factory=list, description="Materials used")
    
    @field_validator("engine_type")
    @classmethod
    def validate_engine_type(cls, v: Optional[str]) -> Optional[str]:
        """Validate engine type."""
        if v is not None:
            valid_types = ["jet", "turboprop", "piston", "turbofan", "turbojet"]
            if v.lower() not in valid_types:
                raise ValueError(f"Engine type must be one of {valid_types}")
            return v.lower()
        return v
    
    # Unit conversion properties
    @property
    def wingspan_m(self) -> float:
        """Wingspan in meters."""
        return self.wingspan * 0.3048
    
    @property
    def wingspan_ft(self) -> float:
        """Wingspan in feet (original unit)."""
        return self.wingspan
    
    @property
    def mtow_kg(self) -> float:
        """MTOW in kilograms."""
        return self.mtow * 0.453592
    
    @property
    def mtow_lb(self) -> float:
        """MTOW in pounds (original unit)."""
        return self.mtow
    
    @property
    def max_speed_kts(self) -> float:
        """Max speed in knots (original unit)."""
        return self.max_speed
    
    @property
    def max_speed_ms(self) -> float:
        """Max speed in meters per second."""
        return self.max_speed * 0.514444
    
    def traverse_components(self):
        """
        Traverse component hierarchy (requires Neo4j backend).
        Returns generator of components.
        """
        # This would be implemented by Neo4j backend
        raise NotImplementedError("Component traversal requires Neo4j backend")
    
    def find_related_materials(self):
        """
        Find all materials used in this aircraft (requires graph backend).
        """
        raise NotImplementedError("Material lookup requires Neo4j backend")


# Forward reference resolution
from .engine import Engine
from .material import Material
Aircraft.model_rebuild()
