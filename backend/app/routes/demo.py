# from fastapi import APIRouter, HTTPException

# from app.database import db
# from app.services.demo_scenario import activate_landslide_scenario
# from app.services.risk_engine import calculate_total_risk
# from app.services.alert_service import create_risk_alert
# from app.services.route_engine import recommend_route


# router = APIRouter(
#     prefix="/demo",
#     tags=["Demo Scenario"]
# )


# @router.post("/landslide/{shipment_id}")
# async def trigger_landslide(shipment_id: str):

#     return await activate_landslide_scenario(
#         shipment_id
#     )


# @router.post("/run-scenario/{shipment_id}")
# async def run_complete_scenario(shipment_id: str):

#     # --------------------------------
#     # 1. Get shipment
#     # --------------------------------

#     shipment = await db.shipments.find_one(
#         {"shipmentId": shipment_id}
#     )

#     if not shipment:
#         raise HTTPException(
#             status_code=404,
#             detail="Shipment not found"
#         )


#     # --------------------------------
#     # 2. Activate landslide
#     # --------------------------------

#     await activate_landslide_scenario(
#         shipment_id
#     )


#     # --------------------------------
#     # 3. Reload shipment
#     # --------------------------------

#     shipment = await db.shipments.find_one(
#         {"shipmentId": shipment_id}
#     )


#     # --------------------------------
#     # 4. Get vehicle
#     # --------------------------------

#     vehicle = await db.vehicles.find_one(
#         {
#             "vehicleId": shipment.get(
#                 "vehicleId"
#             )
#         }
#     )

#     if not vehicle:
#         vehicle = {
#             "currentSpeedKmph": 0
#         }


#     # --------------------------------
#     # 5. Get latest weather
#     # --------------------------------

#     weather = await db.weather_data.find_one(
#         {},
#         sort=[("timestamp", -1)]
#     )

#     if not weather:
#         weather = {}


#     # --------------------------------
#     # 6. Get road condition
#     # --------------------------------

#     road = await db.road_conditions.find_one(
#         {},
#         sort=[("lastInspected", -1)]
#     )

#     if not road:
#         road = {}


#     # --------------------------------
#     # 7. Get active disruptions
#     # --------------------------------

#     disruptions = []

#     cursor = db.disruptions.find(
#         {"status": "ACTIVE"}
#     )

#     async for disruption in cursor:
#         disruptions.append(disruption)


#     # --------------------------------
#     # 8. Calculate risk
#     # --------------------------------

#     risk_result = calculate_total_risk(
#         weather=weather,
#         road=road,
#         disruptions=disruptions,
#         vehicle=vehicle,
#         shipment=shipment
#     )


#     # --------------------------------
#     # 9. Create alert
#     # --------------------------------

#     alert = await create_risk_alert(
#         shipment_id=shipment_id,
#         vehicle_id=shipment.get(
#             "vehicleId"
#         ),
#         risk_result=risk_result
#     )


#     # --------------------------------
#     # 10. Generate route candidates
#     # --------------------------------

#     routes = [
#         {
#             "routeId": "CURRENT",
#             "name": "Current Route",
#             "distanceKm": 250,
#             "estimatedTimeMinutes": 300,
#             "riskScore": risk_result["riskScore"],
#             "riskLevel": risk_result["riskLevel"]
#         },
#         {
#             "routeId": "SAFE-NORTH",
#             "name": "Northern Alternative",
#             "distanceKm": 275,
#             "estimatedTimeMinutes": 330,
#             "riskScore": 28,
#             "riskLevel": "LOW"
#         },
#         {
#             "routeId": "SAFE-SOUTH",
#             "name": "Southern Alternative",
#             "distanceKm": 260,
#             "estimatedTimeMinutes": 315,
#             "riskScore": 47,
#             "riskLevel": "MEDIUM"
#         }
#     ]


#     # --------------------------------
#     # 11. Optimize
#     # --------------------------------

#     route_result = recommend_route(
#         routes
#     )


#     # --------------------------------
#     # 12. Return complete decision
#     # --------------------------------

#     return {
#         "scenario": "LANDSLIDE",
#         "shipmentId": shipment_id,

#         "risk": risk_result,

#         "alert": alert,

#         "routeRecommendation": route_result
#     }

from fastapi import APIRouter
from app.database import db
from app.services.demo_scenario import activate_landslide_scenario
from app.services.risk_engine import calculate_total_risk
from app.services.alert_service import create_risk_alert
from app.services.route_engine import recommend_route


router = APIRouter(
    prefix="/demo",
    tags=["Demo Scenario"]
)


@router.post("/landslide/{shipment_id}")
async def trigger_landslide(shipment_id: str):

    return await activate_landslide_scenario(shipment_id)


@router.post("/run-scenario/{shipment_id}")
async def run_complete_scenario(shipment_id: str):

    # Demo shipment fallback
    shipment = {
        "shipmentId": shipment_id,
        "vehicleId": "V001",
        "origin": "Guwahati",
        "destination": "Shillong",
        "cargoType": "Essential Goods",
        "priority": "HIGH",
        "status": "AT_RISK"
    }

    # Try MongoDB first
    try:
        db_shipment = await db.shipments.find_one(
            {"shipmentId": shipment_id}
        )

        if db_shipment:
            shipment = db_shipment

    except Exception:
        pass


    # Activate landslide
    landslide_result = await activate_landslide_scenario(
        shipment_id
    )


    # Demo vehicle
    vehicle = {
        "vehicleId": "V001",
        "currentSpeedKmph": 28
    }

    try:
        db_vehicle = await db.vehicles.find_one(
            {"vehicleId": shipment.get("vehicleId")}
        )

        if db_vehicle:
            vehicle = db_vehicle

    except Exception:
        pass


    # Demo weather
    weather = {
        "temperature": 24,
        "humidity": 88,
        "rainfall": 18,
        "wind": 14,
        "condition": "Heavy Rain",
        "warning": "Landslide Risk"
    }

    try:
        db_weather = await db.weather_data.find_one(
            {},
            sort=[("timestamp", -1)]
        )

        if db_weather:
            weather = db_weather

    except Exception:
        pass


    # Demo road
    road = {
        "road_id": "R002",
        "name": "Shillong - Cherrapunji Road",
        "status": "Risky",
        "risk_score": 78,
        "passability": "Restricted"
    }

    try:
        db_road = await db.road_conditions.find_one(
            {},
            sort=[("lastInspected", -1)]
        )

        if db_road:
            road = db_road

    except Exception:
        pass


    # Demo active disruption
    disruptions = [
        {
            "type": "LANDSLIDE",
            "severity": "CRITICAL",
            "status": "ACTIVE",
            "location": "NH-15"
        }
    ]

    try:
        cursor = db.disruptions.find(
            {"status": "ACTIVE"}
        )

        db_disruptions = []

        async for disruption in cursor:
            db_disruptions.append(disruption)

        if db_disruptions:
            disruptions = db_disruptions

    except Exception:
        pass


    # Calculate risk
    risk_result = calculate_total_risk(
        weather=weather,
        road=road,
        disruptions=disruptions,
        vehicle=vehicle,
        shipment=shipment
    )


    # Create alert
    try:
        alert = await create_risk_alert(
            shipment_id=shipment_id,
            vehicle_id=shipment.get("vehicleId"),
            risk_result=risk_result
        )

    except Exception:
        alert = {
            "status": "DEMO",
            "severity": risk_result["riskLevel"],
            "message": "Risk alert generated for landslide scenario"
        }


    # Route candidates
    routes = [
        {
            "routeId": "CURRENT",
            "name": "Current Route",
            "distanceKm": 250,
            "estimatedTimeMinutes": 300,
            "riskScore": risk_result["riskScore"],
            "riskLevel": risk_result["riskLevel"]
        },
        {
            "routeId": "SAFE-NORTH",
            "name": "Northern Alternative",
            "distanceKm": 275,
            "estimatedTimeMinutes": 330,
            "riskScore": 28,
            "riskLevel": "LOW"
        },
        {
            "routeId": "SAFE-SOUTH",
            "name": "Southern Alternative",
            "distanceKm": 260,
            "estimatedTimeMinutes": 315,
            "riskScore": 47,
            "riskLevel": "MEDIUM"
        }
    ]


    # Optimize route
    route_result = recommend_route(routes)


    return {
        "scenario": "LANDSLIDE",
        "mode": "DEMO",
        "shipmentId": shipment_id,
        "landslide": landslide_result,
        "risk": risk_result,
        "alert": alert,
        "routeRecommendation": route_result
    }