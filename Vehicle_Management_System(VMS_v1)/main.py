from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel
from typing import Optional, Dict
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
from image_classification import classify_image
from fastapi.responses import JSONResponse
import shutil
import os


class Vehicle(BaseModel):
    id: Optional[int] = None
    make: str
    model: str
    year: int
    price: float
    is_sold: bool = False

vehicles_db: Dict[int, Vehicle] = {}

app = FastAPI()
handler = Mangum(app)

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

@app.post("/classify/")
async def classify_vehicle_image(file: UploadFile = File(...)):
    try:
        # Ensure the temp directory exists
        os.makedirs("temp", exist_ok=True)
        
        # Save the uploaded file to the temp directory
        file_location = f"temp/{file.filename}"
        with open(file_location, "wb+") as file_object:
            shutil.copyfileobj(file.file, file_object)
        
        print(f"File saved to {file_location}")

        # Classify the image
        is_car = classify_image(file_location)
        is_car = bool(is_car)  # Convert NumPy boolean to native Python boolean
        print(f"Classification result: {is_car}")

        # Remove the file after classification
        os.remove(file_location)

        return JSONResponse(content={"is_car": is_car})

    except Exception as e:
        print(f"Error during classification: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Classification error: {str(e)}")