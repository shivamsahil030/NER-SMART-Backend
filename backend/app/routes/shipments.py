# from fastapi import APIRouter, HTTPException
# from pydantic import BaseModel
# from typing import Optional
# from app.database import db


# router = APIRouter(
#     prefix="/shipments",
#     tags=["Shipments"]
# )


# class Location(BaseModel):
#     name: str
#     latitude: float
#     longitude: float


# class ShipmentCreate(BaseModel):
#     shipmentId: str
#     cargoType: str
#     cargoDescription: Optional[str] = None
#     quantity: int
#     unit: str
#     priority: str
#     origin: Location
#     destination: Location
#     vehicleId: str


# @router.get("/")
# async def get_shipments():

#     shipments = []

#     async for shipment in db.shipments.find():
#         shipment["_id"] = str(shipment["_id"])
#         shipments.append(shipment)

#     return {
#         "count": len(shipments),
#         "shipments": shipments
#     }


# @router.get("/{shipment_id}")
# async def get_shipment(shipment_id: str):

#     shipment = await db.shipments.find_one(
#         {"shipmentId": shipment_id}
#     )

#     if not shipment:
#         raise HTTPException(
#             status_code=404,
#             detail="Shipment not found"
#         )

#     shipment["_id"] = str(shipment["_id"])

#     return shipment


# @router.post("/")
# async def create_shipment(shipment: ShipmentCreate):

#     existing_shipment = await db.shipments.find_one(
#         {"shipmentId": shipment.shipmentId}
#     )

#     if existing_shipment:
#         raise HTTPException(
#             status_code=400,
#             detail="Shipment ID already exists"
#         )

#     shipment_data = shipment.model_dump()

#     shipment_data["status"] = "CREATED"

#     shipment_data["route"] = {
#         "currentRouteId": None,
#         "riskScore": 0,
#         "riskLevel": "UNKNOWN",
#         "estimatedTimeMinutes": None
#     }

#     shipment_data["tracking"] = {
#         "currentLocation": None,
#         "speedKmph": 0
#     }

#     result = await db.shipments.insert_one(shipment_data)

#     return {
#         "message": "Shipment created successfully",
#         "shipmentId": shipment.shipmentId,
#         "databaseId": str(result.inserted_id)
#     }

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.database import db


router = APIRouter(
    prefix="/shipments",
    tags=["Shipments"]
)


class Location(BaseModel):
    name: str
    latitude: float
    longitude: float


class ShipmentCreate(BaseModel):
    shipmentId: str
    cargoType: str
    cargoDescription: Optional[str] = None
    quantity: int
    unit: str
    priority: str
    origin: Location
    destination: Location
    vehicleId: str


@router.get("/")
async def get_shipments():

    shipments = []

    try:
        async for shipment in db.shipments.find():
            shipment["_id"] = str(shipment["_id"])
            shipments.append(shipment)

    except Exception:
        shipments = [
            {
                "shipmentId": "1",
                "cargoType": "Essential Goods",
                "cargoDescription": "Food and medical supplies",
                "quantity": 1200,
                "unit": "kg",
                "priority": "HIGH",
                "origin": {
                    "name": "Guwahati",
                    "latitude": 26.1445,
                    "longitude": 91.7362
                },
                "destination": {
                    "name": "Shillong",
                    "latitude": 25.5788,
                    "longitude": 91.8933
                },
                "vehicleId": "V001",
                "status": "IN_TRANSIT",
                "route": {
                    "currentRouteId": "ROUTE-B",
                    "riskScore": 28,
                    "riskLevel": "LOW",
                    "estimatedTimeMinutes": 330
                },
                "tracking": {
                    "currentLocation": {
                        "type": "Point",
                        "coordinates": [91.8933, 25.5788]
                    },
                    "speedKmph": 28
                }
            },
            {
                "shipmentId": "2",
                "cargoType": "Construction Materials",
                "cargoDescription": "Building materials",
                "quantity": 2500,
                "unit": "kg",
                "priority": "MEDIUM",
                "origin": {
                    "name": "Guwahati",
                    "latitude": 26.1445,
                    "longitude": 91.7362
                },
                "destination": {
                    "name": "Tezpur",
                    "latitude": 26.6528,
                    "longitude": 92.7926
                },
                "vehicleId": "V002",
                "status": "CREATED",
                "route": {
                    "currentRouteId": None,
                    "riskScore": 25,
                    "riskLevel": "LOW",
                    "estimatedTimeMinutes": 180
                },
                "tracking": {
                    "currentLocation": None,
                    "speedKmph": 0
                }
            }
        ]

    return {
        "count": len(shipments),
        "shipments": shipments
    }


@router.get("/{shipment_id}")
async def get_shipment(shipment_id: str):

    try:
        shipment = await db.shipments.find_one(
            {"shipmentId": shipment_id}
        )

        if shipment:
            shipment["_id"] = str(shipment["_id"])
            return shipment

    except Exception:
        pass

    demo_shipments = {
        "1": {
            "shipmentId": "1",
            "cargoType": "Essential Goods",
            "cargoDescription": "Food and medical supplies",
            "quantity": 1200,
            "unit": "kg",
            "priority": "HIGH",
            "vehicleId": "V001",
            "status": "IN_TRANSIT"
        },
        "2": {
            "shipmentId": "2",
            "cargoType": "Construction Materials",
            "cargoDescription": "Building materials",
            "quantity": 2500,
            "unit": "kg",
            "priority": "MEDIUM",
            "vehicleId": "V002",
            "status": "CREATED"
        }
    }

    if shipment_id not in demo_shipments:
        raise HTTPException(
            status_code=404,
            detail="Shipment not found"
        )

    return demo_shipments[shipment_id]


@router.post("/")
async def create_shipment(shipment: ShipmentCreate):

    try:
        existing_shipment = await db.shipments.find_one(
            {"shipmentId": shipment.shipmentId}
        )

        if existing_shipment:
            raise HTTPException(
                status_code=400,
                detail="Shipment ID already exists"
            )

        shipment_data = shipment.model_dump()

        shipment_data["status"] = "CREATED"

        shipment_data["route"] = {
            "currentRouteId": None,
            "riskScore": 0,
            "riskLevel": "UNKNOWN",
            "estimatedTimeMinutes": None
        }

        shipment_data["tracking"] = {
            "currentLocation": None,
            "speedKmph": 0
        }

        result = await db.shipments.insert_one(shipment_data)

        return {
            "message": "Shipment created successfully",
            "shipmentId": shipment.shipmentId,
            "databaseId": str(result.inserted_id)
        }

    except HTTPException:
        raise

    except Exception:
        return {
            "message": "Shipment created successfully in demo mode",
            "shipmentId": shipment.shipmentId,
            "status": "CREATED"
        }