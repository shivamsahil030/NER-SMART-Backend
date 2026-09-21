# from fastapi import APIRouter
# from app.database import db


# router = APIRouter(
#     prefix="/disruptions",
#     tags=["Disruptions"]
# )


# @router.get("/")
# async def get_disruptions():

#     disruptions = []

#     async for disruption in db.disruptions.find().sort(
#         "reportedAt", -1
#     ):
#         disruption["_id"] = str(disruption["_id"])
#         disruptions.append(disruption)

#     return {
#         "count": len(disruptions),
#         "disruptions": disruptions
#     }

from fastapi import APIRouter
from pydantic import BaseModel
from datetime import datetime, timezone
from app.database import db

router = APIRouter(
    prefix="/disruptions",
    tags=["Disruptions"]
)


# Demo memory store
DEMO_DISRUPTIONS = [
    {
        "id": "D001",
        "location": "Shillong - Cherrapunji Road",
        "type": "Landslide",
        "severity": "HIGH",
        "status": "ACTIVE",
        "description": "Road partially blocked due to heavy rainfall and landslide.",
        "reportedAt": "2026-09-06T08:30:00"
    },
    {
        "id": "D002",
        "location": "Guwahati - Shillong Highway",
        "type": "Heavy Rain",
        "severity": "MEDIUM",
        "status": "ACTIVE",
        "description": "Heavy rainfall causing reduced visibility and slower traffic.",
        "reportedAt": "2026-09-06T07:45:00"
    },
    {
        "id": "D003",
        "location": "Itanagar - Naharlagun Road",
        "type": "Road Damage",
        "severity": "LOW",
        "status": "MONITORING",
        "description": "Damaged road section reported. Traffic remains open.",
        "reportedAt": "2026-09-06T06:20:00"
    }
]


class DisruptionCreate(BaseModel):
    location: str
    type: str
    severity: str
    status: str = "ACTIVE"
    description: str
    latitude: float | None = None
    longitude: float | None = None
    reportedBy: str | None = None


@router.post("/")
async def create_disruption(disruption: DisruptionCreate):

    disruption_id = f"D-{int(datetime.now().timestamp())}"

    disruption_data = {
        "id": disruption_id,
        "location": disruption.location,
        "type": disruption.type,
        "severity": disruption.severity.upper(),
        "status": disruption.status.upper(),
        "description": disruption.description,
        "latitude": disruption.latitude,
        "longitude": disruption.longitude,
        "reportedBy": disruption.reportedBy or "Field Reporter",
        "reportedAt": datetime.now(timezone.utc).isoformat()
    }

    # DEMO MODE:
    # Do not contact MongoDB. Store the disruption in memory.
    DEMO_DISRUPTIONS.insert(0, disruption_data)

    print("DEMO: Disruption saved:", disruption_data)

    return {
        "message": "Disruption saved successfully",
        "mode": "DEMO",
        "disruption": disruption_data
    }


@router.get("/")
async def get_disruptions():

    try:
        disruptions = []

        async for disruption in db.disruptions.find().sort(
            "reportedAt", -1
        ):
            # Convert ObjectId to string
            if "_id" in disruption:
                disruption["_id"] = str(disruption["_id"])

            disruptions.append(disruption)

        return {
            "count": len(disruptions),
            "disruptions": disruptions
        }

    except Exception:

        return {
            "count": len(DEMO_DISRUPTIONS),
            "disruptions": DEMO_DISRUPTIONS
        }