from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional, Dict, List
from fastapi.middleware.cors import CORSMiddleware
from image_classification import classify_image, classify_angle
import shutil
import os

class Vehicle(BaseModel): #Class Vehicle (Object Oriented Programming)
    id: Optional[int] = None
    make: str
    model: str
    year: int
    price: float
    is_sold: bool = False

vehicles_db: Dict[int, Vehicle] = {} #Data type : Dictionary

os.makedirs("temp", exist_ok=True)

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/temp", StaticFiles(directory="temp"), name="temp")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],
)

#RESTful API Endpoints (CRUD Operations) listed below
# POST, GET, PUT, DELETE HTTP endpoints for vehicles to perform CRUD operations
#FastAPI is a web framework. here async and await are used to make the code asynchronous
@app.post("/vehicles/") #Decorator 
async def create_vehicle(vehicle: Vehicle): #Endpoint Function
    vehicle.id = len(vehicles_db) + 1
    vehicles_db[vehicle.id] = vehicle
    return vehicles_db[vehicle.id]

@app.get("/vehicles/") #Decorator
async def read_vehicles():
    return vehicles_db

@app.get("/vehicles/{vehicle_id}") #Decorator
async def read_vehicle(vehicle_id: int): #Endpoint Function
    vehicle = vehicles_db.get(vehicle_id)
    if vehicle is None: #Control Flow : If statement
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return vehicle

@app.put("/vehicles/{vehicle_id}") #Decorator
async def update_vehicle(vehicle_id: int, vehicle: Vehicle): #Endpoint Function
    if vehicle_id not in vehicles_db: #Control Flow : If statement
        raise HTTPException(status_code=404, detail="Vehicle not found")
    vehicles_db[vehicle_id] = vehicle
    return vehicles_db[vehicle_id]

@app.delete("/vehicles/{vehicle_id}") #Decorator
async def delete_vehicle(vehicle_id: int):
    if vehicle_id not in vehicles_db: #Control Flow : If statement  
        raise HTTPException(status_code=404, detail="Vehicle not found")
    del vehicles_db[vehicle_id]
    return {"message": "Vehicle deleted successfully"}

@app.put("/vehicles/{vehicle_id}/sold") #Decorator
async def mark_vehicle_as_sold(vehicle_id: int):
    if vehicle_id not in vehicles_db:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    vehicles_db[vehicle_id].is_sold = True
    return vehicles_db[vehicle_id]

@app.post("/classify/") #Decorator
async def classify_vehicle_image(file: UploadFile = File(...)):
    try: #Exception Handling : try block
        # Ensure the temp directory exists
        os.makedirs("temp", exist_ok=True)
        
        # Save the uploaded file to the temp directory
        file_location = f"temp/{file.filename}"
        with open(file_location, "wb+") as file_object: #File I/O Operations: Open file in write mode
            shutil.copyfileobj(file.file, file_object)
        
        print(f"File saved to {file_location}")

        # Classify the image
        is_car = classify_image(file_location)
        is_car = bool(is_car)  # Convert NumPy boolean to native Python boolean
        print(f"Classification result: {is_car}")

        # Remove the file after classification
        os.remove(file_location) #File I/O Operations: Remove file

        return JSONResponse(content={"is_car": is_car})

    except Exception as e: #Exception Handling : except block
        print(f"Error during classification: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Classification error: {str(e)}")
    
@app.get("/", response_class=HTMLResponse) #Decorator
async def read_index():
    with open("index.html") as f: #File I/O Operations: Open file in read mode
        return HTMLResponse(content=f.read(), media_type="text/html")
        
@app.post("/classify_angle/") #Decorator
async def classify_vehicle_angles(files: List[UploadFile] = File(...)): #Data type : List
    results = {'front': [], 'left': [], 'right': [], 'back': []} #Data type : Dictionary of Datatype List
    try: #Exception Handling : try block
        for file in files: #Control Flow : For loop
            # Save the uploaded file to the temp directory
            file_location = f"temp/{file.filename}"
            with open(file_location, "wb+") as file_object: #Context Manager: Open file
                shutil.copyfileobj(file.file, file_object)
            
            print(f"File saved to {file_location}")

            # Classify the image angle
            angle = classify_angle(file_location)
            print(f"Classification result for {file.filename}: {angle}")

            # Store the result
            results[angle].append(file.filename)

        # Sort results by angle
        sorted_results = {angle: results[angle] for angle in sorted(results)}

        return JSONResponse(content=sorted_results)

    except Exception as e: #Exception Handling : except block
        print(f"Error during classification: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Classification error: {str(e)}")
