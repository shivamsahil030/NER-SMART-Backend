# from fastapi import APIRouter, HTTPException

# from app.database import db
# from app.services.risk_engine import calculate_total_risk
# from app.services.alert_service import create_risk_alert


# router = APIRouter(
#     prefix="/risk",
#     tags=["Risk Engine"]
# )


# @router.get("/{shipment_id}")
# async def calculate_shipment_risk(shipment_id: str):

#     # Get shipment
#     shipment = await db.shipments.find_one(
#         {"shipmentId": shipment_id}
#     )

#     if not shipment:
#         raise HTTPException(
#             status_code=404,
#             detail="Shipment not found"
#         )

#     # Get vehicle
#     vehicle = await db.vehicles.find_one(
#         {"vehicleId": shipment.get("vehicleId")}
#     )

#     if not vehicle:
#         vehicle = {
#             "currentSpeedKmph": 0
#         }

#     # Get latest weather
#     weather = await db.weather_data.find_one(
#         {},
#         sort=[("timestamp", -1)]
#     )

#     if not weather:
#         weather = {}

#     # Get latest road condition
#     road = await db.road_conditions.find_one(
#         {},
#         sort=[("lastInspected", -1)]
#     )

#     if not road:
#         road = {}

#     # Get active disruptions
#     disruptions = []

#     cursor = db.disruptions.find(
#         {"status": "ACTIVE"}
#     )

#     async for disruption in cursor:
#         disruptions.append(disruption)

#     # Calculate risk
#     result = calculate_total_risk(
#         weather=weather,
#         road=road,
#         disruptions=disruptions,
#         vehicle=vehicle,
#         shipment=shipment
        
#     )
#     alert = await create_risk_alert(
#         shipment_id=shipment_id,
#         vehicle_id=shipment.get("vehicleId"),
#         risk_result=result
#     )
    
#     return {
#         "shipmentId": shipment_id,
#         **result,
#         "alert": alert
#     }

from fastapi import APIRouter
from app.database import db
from app.services.risk_engine import calculate_total_risk
from app.routes.disruptions import DEMO_DISRUPTIONS
from app.services.alert_service import create_risk_alert


router = APIRouter(
    prefix="/risk",
    tags=["Risk Engine"]
)


@router.get("/{shipment_id}")
async def calculate_shipment_risk(shipment_id: str):

    try:
        # Get shipment from MongoDB
        shipment = await db.shipments.find_one(
            {"shipmentId": shipment_id}
        )

        # Demo shipment fallback
        if not shipment:
            shipment = {
                "shipmentId": shipment_id,
                "vehicleId": "V001",
                "origin": "Guwahati",
                "destination": "Shillong",
                "cargoType": "General Goods"
            }

        # Get vehicle
        vehicle = await db.vehicles.find_one(
            {"vehicleId": shipment.get("vehicleId")}
        )

        if not vehicle:
            vehicle = {
                "vehicleId": shipment.get("vehicleId"),
                "currentSpeedKmph": 35
            }

        # Get latest weather
        weather = await db.weather_data.find_one(
            {},
            sort=[("timestamp", -1)]
        )

        if not weather:
            weather = {
                "temperature": 24,
                "humidity": 88,
                "rainfall": 12,
                "wind": 14,
                "condition": "Heavy Rain",
                "warning": "Monsoon Alert Level 3"
            }

        # Get latest road condition
        road = await db.road_conditions.find_one(
            {},
            sort=[("lastInspected", -1)]
        )

        if not road:
            road = {
                "road_id": "R001",
                "name": "Guwahati - Shillong Highway",
                "status": "Caution",
                "risk_score": 65,
                "passability": "Passable"
            }

        # Get active disruptions
        disruptions = []

        cursor = db.disruptions.find(
            {"status": "ACTIVE"}
        )

        async for disruption in cursor:
            disruptions.append(disruption)

    except Exception:
        # Complete demo fallback when MongoDB is unavailable

        shipment = {
            "shipmentId": shipment_id,
            "vehicleId": "V001",
            "origin": "Guwahati",
            "destination": "Shillong",
            "cargoType": "General Goods"
        }

        vehicle = {
            "vehicleId": "V001",
            "currentSpeedKmph": 35
        }

        weather = {
            "temperature": 24,
            "humidity": 88,
            "rainfall": 12,
            "wind": 14,
            "condition": "Heavy Rain",
            "warning": "Monsoon Alert Level 3"
        }

        road = {
            "road_id": "R001",
            "name": "Guwahati - Shillong Highway",
            "status": "Caution",
            "risk_score": 65,
            "passability": "Passable"
        }

        disruptions = DEMO_DISRUPTIONS

    # Calculate risk
    result = calculate_total_risk(
        weather=weather,
        road=road,
        disruptions=disruptions,
        vehicle=vehicle,
        shipment=shipment
    )

    # Try to create alert, but don't let MongoDB failure break the API
    try:
        alert = await create_risk_alert(
            shipment_id=shipment_id,
            vehicle_id=shipment.get("vehicleId"),
            risk_result=result
        )
    except Exception:
        alert = {
            "status": "DEMO",
            "message": "Risk alert generated in demo mode"
        }

    return {
        "shipmentId": shipment_id,
        **result,
        "alert": alert
    }