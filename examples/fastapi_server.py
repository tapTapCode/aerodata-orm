"""
FastAPI server example showing AeroData ORM integration.
"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from typing import List, Optional
from aerodata_orm import Aircraft, Engine, Material, SQLAlchemyBackend

# Initialize FastAPI app
app = FastAPI(
    title="AeroData ORM API",
    description="REST API for aerospace engineering data",
    version="1.0.0"
)

# Initialize database backend
backend = SQLAlchemyBackend("postgresql://localhost/aerospace_db")


@app.on_event("startup")
async def startup():
    """Connect to database on startup."""
    backend.connect()


@app.on_event("shutdown")
async def shutdown():
    """Disconnect from database on shutdown."""
    backend.disconnect()


@app.get("/aircraft", response_model=List[dict])
async def list_aircraft(
    manufacturer: Optional[str] = None,
    min_speed: Optional[int] = None,
    max_altitude: Optional[int] = None,
    limit: int = 100
):
    """
    List aircraft with optional filters.
    
    Example:
        GET /aircraft?manufacturer=Boeing&min_speed=500
    """
    query = Aircraft.query(backend)
    
    if manufacturer:
        query = query.where(manufacturer=manufacturer)
    if min_speed:
        query = query.where(max_speed__gte=min_speed)
    if max_altitude:
        query = query.where(max_altitude__gte=max_altitude)
    
    aircraft_list = query.limit(limit).all()
    return [a.to_dict() for a in aircraft_list]


@app.get("/aircraft/{aircraft_id}", response_model=dict)
async def get_aircraft(aircraft_id: int):
    """
    Get a specific aircraft by ID.
    
    Example:
        GET /aircraft/123
    """
    aircraft = Aircraft.get_by_id(backend, aircraft_id)
    if not aircraft:
        raise HTTPException(status_code=404, detail="Aircraft not found")
    return aircraft.to_dict()


@app.post("/aircraft", response_model=dict, status_code=201)
async def create_aircraft(aircraft_data: dict):
    """
    Create a new aircraft.
    
    Example:
        POST /aircraft
        {
            "model": "737-800",
            "manufacturer": "Boeing",
            "max_speed": 544,
            "max_altitude": 41000,
            "wingspan": 117.5,
            "length": 129.5,
            "mtow": 174200
        }
    """
    aircraft = Aircraft(**aircraft_data)
    aircraft.save(backend)
    return {"id": aircraft.id, "model": aircraft.model}


@app.get("/engines", response_model=List[dict])
async def list_engines(manufacturer: Optional[str] = None, limit: int = 100):
    """
    List engines with optional filters.
    """
    query = Engine.query(backend)
    
    if manufacturer:
        query = query.where(manufacturer=manufacturer)
    
    engines = query.limit(limit).all()
    return [e.to_dict() for e in engines]


@app.get("/materials", response_model=List[dict])
async def list_materials(
    category: Optional[str] = None,
    min_tensile_strength: Optional[float] = None,
    limit: int = 100
):
    """
    List materials with optional filters.
    """
    query = Material.query(backend)
    
    if category:
        query = query.where(category=category)
    if min_tensile_strength:
        query = query.where(tensile_strength__gte=min_tensile_strength)
    
    materials = query.limit(limit).all()
    return [m.to_dict() for m in materials]


@app.get("/aircraft/{aircraft_id}/engines", response_model=List[dict])
async def get_aircraft_engines(aircraft_id: int):
    """
    Get all engines for a specific aircraft.
    """
    aircraft = Aircraft.query(backend) \
        .where(id=aircraft_id) \
        .with_engines() \
        .first()
    
    if not aircraft:
        raise HTTPException(status_code=404, detail="Aircraft not found")
    
    return [e.to_dict() for e in aircraft.engines]


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
