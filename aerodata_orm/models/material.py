"""
Material model for aerospace materials with ASTM/ISO standards.
"""

from typing import Optional, Tuple
from pydantic import Field, field_validator
from .base import BaseModel


class Material(BaseModel):
    """
    Aerospace material model with properties and standards validation.
    """
    
    name: str = Field(..., description="Material name (e.g., Aluminum 7075-T6)")
    specification: Optional[str] = Field(None, description="Material specification")
    astm_grade: Optional[str] = Field(None, description="ASTM grade/standard (e.g., B209)")
    
    # Physical properties
    density: float = Field(..., description="Density in g/cm³", gt=0)
    
    # Mechanical properties (in MPa)
    tensile_strength: float = Field(..., description="Ultimate tensile strength in MPa", gt=0)
    yield_strength: float = Field(..., description="Yield strength in MPa", gt=0)
    elastic_modulus: float = Field(..., description="Elastic modulus (Young's) in GPa", gt=0)
    
    # Thermal properties
    melting_point: Optional[float] = Field(None, description="Melting point in °C")
    thermal_conductivity: Optional[float] = Field(
        None, 
        description="Thermal conductivity in W/(m·K)", 
        gt=0
    )
    thermal_expansion: Optional[float] = Field(
        None, 
        description="Coefficient of thermal expansion in μm/(m·°C)", 
        gt=0
    )
    
    # Temperature rating (min, max) in Celsius
    temperature_rating: Optional[Tuple[float, float]] = Field(
        None, 
        description="Operating temperature range (min, max) in °C"
    )
    
    # Chemical composition
    primary_element: Optional[str] = Field(None, description="Primary element (Al, Ti, Steel, etc.)")
    alloy_composition: Optional[str] = Field(None, description="Alloy composition description")
    
    # Metadata
    category: Optional[str] = Field(
        None, 
        description="Material category (metal, composite, polymer, ceramic)"
    )
    
    @field_validator("astm_grade")
    @classmethod
    def validate_astm_grade(cls, v: Optional[str]) -> Optional[str]:
        """Validate ASTM grade format."""
        if v is not None:
            # Basic ASTM format validation (letter + numbers)
            if not v[0].isalpha() or not any(c.isdigit() for c in v):
                raise ValueError(
                    f"ASTM grade '{v}' should start with letter followed by numbers (e.g., B209)"
                )
        return v
    
    @field_validator("temperature_rating")
    @classmethod
    def validate_temperature_range(cls, v: Optional[Tuple[float, float]]) -> Optional[Tuple[float, float]]:
        """Validate temperature range."""
        if v is not None:
            min_temp, max_temp = v
            if min_temp >= max_temp:
                raise ValueError(f"Min temperature ({min_temp}) must be less than max ({max_temp})")
            if min_temp < -273:  # Absolute zero
                raise ValueError(f"Min temperature cannot be below absolute zero")
        return v
    
    @field_validator("category")
    @classmethod
    def validate_category(cls, v: Optional[str]) -> Optional[str]:
        """Validate material category."""
        if v is not None:
            valid_categories = ["metal", "composite", "polymer", "ceramic", "alloy"]
            if v.lower() not in valid_categories:
                raise ValueError(f"Category must be one of {valid_categories}")
            return v.lower()
        return v
    
    # Unit conversion properties
    @property
    def density_kg_m3(self) -> float:
        """Density in kg/m³."""
        return self.density * 1000
    
    @property
    def tensile_strength_psi(self) -> float:
        """Tensile strength in PSI."""
        return self.tensile_strength * 145.038
    
    @property
    def yield_strength_psi(self) -> float:
        """Yield strength in PSI."""
        return self.yield_strength * 145.038
