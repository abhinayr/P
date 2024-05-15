from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict
from fastapi.middleware.cors import CORSMiddleware

class Vehicle(BaseModel):
    id: Optional[int] = None
    make: str
    model: str
    year: int
    price: float
    is_sold: bool = False

vehicles_db: Dict[int, Vehicle] = {}

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],
)

@app.post("/vehicles/")
async def create_vehicle(vehicle: Vehicle):
    vehicle.id = len(vehicles_db) + 1
    vehicles_db[vehicle.id] = vehicle
    return vehicles_db[vehicle.id]

@app.get("/vehicles/")
async def read_vehicles():
    return vehicles_db

@app.get("/vehicles/{vehicle_id}")
async def read_vehicle(vehicle_id: int):
    vehicle = vehicles_db.get(vehicle_id)
    if vehicle is None:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return vehicle

@app.put("/vehicles/{vehicle_id}")
async def update_vehicle(vehicle_id: int, vehicle: Vehicle):
    if vehicle_id not in vehicles_db:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    vehicles_db[vehicle_id] = vehicle
    return vehicles_db[vehicle_id]

@app.delete("/vehicles/{vehicle_id}")
async def delete_vehicle(vehicle_id: int):
    if vehicle_id not in vehicles_db:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    del vehicles_db[vehicle_id]
    return {"message": "Vehicle deleted successfully"}

@app.put("/vehicles/{vehicle_id}/sold")
async def mark_vehicle_as_sold(vehicle_id: int):
    if vehicle_id not in vehicles_db:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    vehicles_db[vehicle_id].is_sold = True
    return vehicles_db[vehicle_id]