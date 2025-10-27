"""
Engine model for aerospace data.
"""

from typing import Optional
from pydantic import Field
from .base import BaseModel


class Engine(BaseModel):
    """
    Engine model with performance and specifications.
    """
    
    model: str = Field(..., description="Engine model designation (e.g., CFM56-7B, GE90)")
    manufacturer: str = Field(..., description="Engine manufacturer (e.g., CFM, GE, P&W)")
    
    # Type
    engine_type: str = Field(..., description="Engine type (turbofan, turbojet, turboprop)")
    
    # Performance
    thrust: float = Field(..., description="Maximum thrust in pounds-force (lbf)", gt=0)
    specific_fuel_consumption: Optional[float] = Field(
        None, 
        description="Specific fuel consumption (lb/lbf/hr)", 
        gt=0
    )
    bypass_ratio: Optional[float] = Field(None, description="Bypass ratio", ge=0)
    
    # Physical specs
    weight: float = Field(..., description="Dry weight in pounds", gt=0)
    length: Optional[float] = Field(None, description="Length in inches", gt=0)
    diameter: Optional[float] = Field(None, description="Fan diameter in inches", gt=0)
    
    # Operational
    max_rpm: Optional[int] = Field(None, description="Maximum RPM", gt=0)
    compression_ratio: Optional[float] = Field(None, description="Overall compression ratio", gt=1)
    
    # Metadata
    first_run: Optional[str] = Field(None, description="First run date (YYYY-MM-DD)")
    production_status: Optional[str] = Field(None, description="Production status")
    
    # Unit conversion properties
    @property
    def thrust_kn(self) -> float:
        """Thrust in kilonewtons."""
        return self.thrust * 0.00444822
    
    @property
    def thrust_lbf(self) -> float:
        """Thrust in pounds-force (original unit)."""
        return self.thrust
    
    @property
    def weight_kg(self) -> float:
        """Weight in kilograms."""
        return self.weight * 0.453592
    
    @property
    def weight_lb(self) -> float:
        """Weight in pounds (original unit)."""
        return self.weight
