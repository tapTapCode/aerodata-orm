"""
Flight data model for tracking flights and telemetry.
"""

from typing import Optional
from datetime import datetime
from pydantic import Field
from .base import BaseModel


class FlightData(BaseModel):
    """
    Flight data model for tracking flights and performance.
    """
    
    flight_number: str = Field(..., description="Flight number (e.g., AA123)")
    aircraft_id: int = Field(..., description="Aircraft ID (foreign key)")
    
    # Route
    origin: str = Field(..., description="Origin airport code (ICAO)")
    destination: str = Field(..., description="Destination airport code (ICAO)")
    
    # Timing
    departure_date: datetime = Field(..., description="Departure date and time (UTC)")
    arrival_date: Optional[datetime] = Field(None, description="Arrival date and time (UTC)")
    flight_time: Optional[int] = Field(None, description="Flight time in minutes", ge=0)
    
    # Performance
    distance: Optional[float] = Field(None, description="Flight distance in nautical miles", gt=0)
    fuel_used: Optional[float] = Field(None, description="Fuel used in gallons", ge=0)
    avg_speed: Optional[float] = Field(None, description="Average ground speed in knots", gt=0)
    max_altitude_reached: Optional[float] = Field(
        None, 
        description="Maximum altitude reached in feet", 
        ge=0
    )
    
    # Capacity
    passengers: Optional[int] = Field(None, description="Number of passengers", ge=0)
    cargo_weight: Optional[float] = Field(None, description="Cargo weight in pounds", ge=0)
    
    # Status
    status: str = Field(
        default="scheduled", 
        description="Flight status (scheduled, departed, arrived, cancelled)"
    )
    
    # Relationships (loaded via query.with_aircraft())
    aircraft: Optional["Aircraft"] = Field(None, description="Associated aircraft")
    
    @property
    def distance_km(self) -> Optional[float]:
        """Distance in kilometers."""
        if self.distance:
            return self.distance * 1.852
        return None
    
    @property
    def fuel_used_liters(self) -> Optional[float]:
        """Fuel used in liters."""
        if self.fuel_used:
            return self.fuel_used * 3.78541
        return None


# Forward reference resolution
from .aircraft import Aircraft
FlightData.model_rebuild()
