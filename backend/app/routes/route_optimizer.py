from fastapi import APIRouter
from pydantic import BaseModel

from app.services.route_engine import recommend_route
from app.routes.risk import calculate_shipment_risk


router = APIRouter(
    prefix="/route",
    tags=["Route Optimization"]
)


class RouteRequest(BaseModel):
    shipmentId: str


@router.post("/recommend")
async def recommend(request: RouteRequest):

    # ---------------------------------
    # Get latest risk from Risk Engine
    # ---------------------------------

    risk_data = await calculate_shipment_risk(
        request.shipmentId
    )

    current_risk_score = risk_data.get(
        "riskScore",
        50
    )

    current_risk_level = risk_data.get(
        "riskLevel",
        "MEDIUM"
    )

    # ---------------------------------
    # Candidate Routes
    # ---------------------------------

    candidate_routes = [
        {
            "routeId": "ROUTE-A",
            "name": "Current Route",
            "distanceKm": 250,
            "estimatedTimeMinutes": 300,
            "riskScore": current_risk_score,
            "riskLevel": current_risk_level,
            "waypoints": []
        },
        {
            "routeId": "ROUTE-B",
            "name": "Alternative North",
            "distanceKm": 275,
            "estimatedTimeMinutes": 330,
            "riskScore": 15,
            "riskLevel": "LOW",
            "waypoints": ["Tezpur, Assam"]
        },
        {
            "routeId": "ROUTE-C",
            "name": "Alternative South",
            "distanceKm": 260,
            "estimatedTimeMinutes": 315,
            "riskScore": 35,
            "riskLevel": "MEDIUM",
            "waypoints": ["Nagaon, Assam"]
        }
    ]

    # ---------------------------------
    # Optimize Routes
    # ---------------------------------

    result = recommend_route(
        candidate_routes
    )

    return {
        "shipmentId": request.shipmentId,
        "currentRisk": {
            "riskScore": current_risk_score,
            "riskLevel": current_risk_level
        },
        "recommendation": result
    }