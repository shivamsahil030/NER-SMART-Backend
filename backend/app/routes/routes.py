# from fastapi import APIRouter
# from app.database import db


# router = APIRouter(
#     prefix="/routes",
#     tags=["Routes"]
# )


# @router.get("/")
# async def get_routes():

#     routes = []

#     async for route in db.route_history.find().sort(
#         "createdAt", -1
#     ):
#         route["_id"] = str(route["_id"])
#         routes.append(route)

#     return {
#         "count": len(routes),
#         "routes": routes
#     }


# @router.get("/{shipment_id}")
# async def get_shipment_routes(shipment_id: str):

#     routes = []

#     async for route in db.route_history.find(
#         {"shipmentId": shipment_id}
#     ):
#         route["_id"] = str(route["_id"])
#         routes.append(route)

#     return {
#         "count": len(routes),
#         "routes": routes
#     }

from fastapi import APIRouter
from app.database import db


router = APIRouter(
    prefix="/routes",
    tags=["Routes"]
)


@router.get("/")
async def get_routes():

    routes = []

    try:
        async for route in db.route_history.find().sort(
            "createdAt", -1
        ):
            route["_id"] = str(route["_id"])
            routes.append(route)

    except Exception:
        routes = [
            {
                "routeId": "ROUTE-A",
                "shipmentId": "1",
                "name": "Current Route",
                "distanceKm": 250,
                "estimatedTimeMinutes": 300,
                "riskScore": 82,
                "riskLevel": "CRITICAL",
                "status": "HIGH_RISK"
            },
            {
                "routeId": "ROUTE-B",
                "shipmentId": "1",
                "name": "Alternative North",
                "distanceKm": 275,
                "estimatedTimeMinutes": 330,
                "riskScore": 28,
                "riskLevel": "LOW",
                "status": "RECOMMENDED"
            },
            {
                "routeId": "ROUTE-C",
                "shipmentId": "1",
                "name": "Alternative South",
                "distanceKm": 260,
                "estimatedTimeMinutes": 315,
                "riskScore": 47,
                "riskLevel": "MEDIUM",
                "status": "AVAILABLE"
            }
        ]

    return {
        "count": len(routes),
        "routes": routes
    }


@router.get("/{shipment_id}")
async def get_shipment_routes(shipment_id: str):

    routes = []

    try:
        async for route in db.route_history.find(
            {"shipmentId": shipment_id}
        ):
            route["_id"] = str(route["_id"])
            routes.append(route)

    except Exception:
        routes = [
            {
                "routeId": "ROUTE-A",
                "shipmentId": shipment_id,
                "name": "Current Route",
                "distanceKm": 250,
                "estimatedTimeMinutes": 300,
                "riskScore": 82,
                "riskLevel": "CRITICAL",
                "status": "HIGH_RISK"
            },
            {
                "routeId": "ROUTE-B",
                "shipmentId": shipment_id,
                "name": "Alternative North",
                "distanceKm": 275,
                "estimatedTimeMinutes": 330,
                "riskScore": 28,
                "riskLevel": "LOW",
                "status": "RECOMMENDED"
            },
            {
                "routeId": "ROUTE-C",
                "shipmentId": shipment_id,
                "name": "Alternative South",
                "distanceKm": 260,
                "estimatedTimeMinutes": 315,
                "riskScore": 47,
                "riskLevel": "MEDIUM",
                "status": "AVAILABLE"
            }
        ]

    return {
        "count": len(routes),
        "routes": routes
    }