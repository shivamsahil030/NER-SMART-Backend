# from fastapi import APIRouter, HTTPException
# from pydantic import BaseModel
# from typing import Optional
# from app.database import db


# router = APIRouter(
#     prefix="/vehicles",
#     tags=["Vehicles"]
# )


# class VehicleCreate(BaseModel):
#     vehicleId: str
#     vehicleNumber: str
#     vehicleType: str
#     driverName: str
#     capacityKg: float
#     status: str = "AVAILABLE"


# @router.get("/")
# async def get_vehicles():

#     vehicles = []

#     async for vehicle in db.vehicles.find():
#         vehicle["_id"] = str(vehicle["_id"])
#         vehicles.append(vehicle)

#     return {
#         "count": len(vehicles),
#         "vehicles": vehicles
#     }


# @router.get("/{vehicle_id}")
# async def get_vehicle(vehicle_id: str):

#     vehicle = await db.vehicles.find_one(
#         {"vehicleId": vehicle_id}
#     )

#     if not vehicle:
#         raise HTTPException(
#             status_code=404,
#             detail="Vehicle not found"
#         )

#     vehicle["_id"] = str(vehicle["_id"])

#     return vehicle


# @router.post("/")
# async def create_vehicle(vehicle: VehicleCreate):

#     existing = await db.vehicles.find_one(
#         {"vehicleId": vehicle.vehicleId}
#     )

#     if existing:
#         raise HTTPException(
#             status_code=400,
#             detail="Vehicle ID already exists"
#         )

#     data = vehicle.model_dump()

#     data["currentLocation"] = None
#     data["currentSpeedKmph"] = 0
#     data["assignedShipmentId"] = None

#     result = await db.vehicles.insert_one(data)

#     return {
#         "message": "Vehicle created successfully",
#         "vehicleId": vehicle.vehicleId,
#         "databaseId": str(result.inserted_id)
#     }

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.database import db


router = APIRouter(
    prefix="/vehicles",
    tags=["Vehicles"]
)


class VehicleCreate(BaseModel):
    vehicleId: str
    vehicleNumber: str
    vehicleType: str
    driverName: str
    capacityKg: float
    status: str = "AVAILABLE"


@router.get("/")
async def get_vehicles():

    vehicles = []

    try:
        async for vehicle in db.vehicles.find():
            vehicle["_id"] = str(vehicle["_id"])
            vehicles.append(vehicle)

    except Exception:
        # Demo vehicles when MongoDB is unavailable
        vehicles = [
            {
                "vehicleId": "V001",
                "vehicleNumber": "AS01AB1234",
                "vehicleType": "Truck",
                "driverName": "Demo Driver",
                "capacityKg": 5000,
                "status": "ON_ROUTE",
                "currentLocation": {
                    "type": "Point",
                    "coordinates": [91.8933, 25.5788]
                },
                "currentSpeedKmph": 28,
                "assignedShipmentId": "1"
            },
            {
                "vehicleId": "V002",
                "vehicleNumber": "ML05CD5678",
                "vehicleType": "Cargo Van",
                "driverName": "Demo Driver 2",
                "capacityKg": 2500,
                "status": "AVAILABLE",
                "currentLocation": {
                    "type": "Point",
                    "coordinates": [91.7362, 26.1445]
                },
                "currentSpeedKmph": 0,
                "assignedShipmentId": None
            },
            {
                "vehicleId": "V003",
                "vehicleNumber": "AR01EF9012",
                "vehicleType": "Truck",
                "driverName": "Demo Driver 3",
                "capacityKg": 7500,
                "status": "MAINTENANCE",
                "currentLocation": None,
                "currentSpeedKmph": 0,
                "assignedShipmentId": None
            }
        ]

    return {
        "count": len(vehicles),
        "vehicles": vehicles
    }


@router.get("/{vehicle_id}")
async def get_vehicle(vehicle_id: str):

    try:
        vehicle = await db.vehicles.find_one(
            {"vehicleId": vehicle_id}
        )

        if vehicle:
            vehicle["_id"] = str(vehicle["_id"])
            return vehicle

    except Exception:
        pass

    # Demo vehicle fallback
    demo_vehicles = {
        "V001": {
            "vehicleId": "V001",
            "vehicleNumber": "AS01AB1234",
            "vehicleType": "Truck",
            "driverName": "Demo Driver",
            "capacityKg": 5000,
            "status": "ON_ROUTE",
            "currentSpeedKmph": 28,
            "assignedShipmentId": "1"
        },
        "V002": {
            "vehicleId": "V002",
            "vehicleNumber": "ML05CD5678",
            "vehicleType": "Cargo Van",
            "driverName": "Demo Driver 2",
            "capacityKg": 2500,
            "status": "AVAILABLE",
            "currentSpeedKmph": 0,
            "assignedShipmentId": None
        }
    }

    if vehicle_id in demo_vehicles:
        return demo_vehicles[vehicle_id]

    raise HTTPException(
        status_code=404,
        detail="Vehicle not found"
    )


@router.post("/")
async def create_vehicle(vehicle: VehicleCreate):

    try:
        existing = await db.vehicles.find_one(
            {"vehicleId": vehicle.vehicleId}
        )

        if existing:
            raise HTTPException(
                status_code=400,
                detail="Vehicle ID already exists"
            )

        data = vehicle.model_dump()

        data["currentLocation"] = None
        data["currentSpeedKmph"] = 0
        data["assignedShipmentId"] = None

        result = await db.vehicles.insert_one(data)

        return {
            "message": "Vehicle created successfully",
            "vehicleId": vehicle.vehicleId,
            "databaseId": str(result.inserted_id)
        }

    except HTTPException:
        raise

    except Exception:
        # Demo mode
        return {
            "message": "Vehicle created successfully in demo mode",
            "vehicleId": vehicle.vehicleId,
            "status": "DEMO"
        }