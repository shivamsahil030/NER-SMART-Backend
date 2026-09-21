# from fastapi import APIRouter
# from app.database import db


# router = APIRouter(
#     prefix="/alerts",
#     tags=["Alerts"]
# )


# @router.get("/")
# async def get_alerts():

#     alerts = []

#     cursor = db.alerts.find(
#         {"status": "ACTIVE"}
#     ).sort("createdAt", -1)

#     async for alert in cursor:
#         alert["_id"] = str(alert["_id"])
#         alerts.append(alert)

#     return {
#         "count": len(alerts),
#         "alerts": alerts
#     }

from fastapi import APIRouter
from app.database import db


router = APIRouter(
    prefix="/alerts",
    tags=["Alerts"]
)


@router.get("/")
async def get_alerts():

    alerts = []

    try:
        cursor = db.alerts.find(
            {"status": "ACTIVE"}
        ).sort("createdAt", -1)

        async for alert in cursor:
            alert["_id"] = str(alert["_id"])
            alerts.append(alert)

    except Exception:
        # Fallback demo alerts if MongoDB is unavailable
        alerts = [
            {
                "id": "A001",
                "type": "LANDSLIDE",
                "severity": "HIGH",
                "title": "Landslide Risk Alert",
                "message": "High landslide risk detected on Shillong - Cherrapunji Road.",
                "location": "Shillong - Cherrapunji Road",
                "status": "ACTIVE",
                "createdAt": "2026-09-06T08:30:00"
            },
            {
                "id": "A002",
                "type": "WEATHER",
                "severity": "MEDIUM",
                "title": "Heavy Rain Alert",
                "message": "Heavy rainfall may cause delays on Guwahati - Shillong Highway.",
                "location": "Guwahati - Shillong Highway",
                "status": "ACTIVE",
                "createdAt": "2026-09-06T07:45:00"
            },
            {
                "id": "A003",
                "type": "ROAD",
                "severity": "LOW",
                "title": "Road Condition Alert",
                "message": "Damaged road section reported near Itanagar - Naharlagun.",
                "location": "Itanagar - Naharlagun Road",
                "status": "ACTIVE",
                "createdAt": "2026-09-06T06:20:00"
            }
        ]

    return {
        "count": len(alerts),
        "alerts": alerts
    }