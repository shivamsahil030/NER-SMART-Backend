# from fastapi import APIRouter
# from pydantic import BaseModel
# from datetime import datetime, timezone
# from app.database import db


# router = APIRouter(
#     prefix="/events",
#     tags=["Shipment Events"]
# )


# class EventCreate(BaseModel):
#     shipmentId: str
#     vehicleId: str | None = None
#     eventType: str
#     description: str
#     locationName: str


# @router.post("/")
# async def create_event(event: EventCreate):

#     event_data = {
#         "eventId": f"EVT-{int(datetime.now().timestamp())}",
#         "shipmentId": event.shipmentId,
#         "vehicleId": event.vehicleId,
#         "eventType": event.eventType,
#         "description": event.description,
#         "locationName": event.locationName,
#         "timestamp": datetime.now(timezone.utc),
#         "blockchain": {
#             "status": "PENDING",
#             "transactionId": None
#         }
#     }

#     result = await db.shipment_events.insert_one(event_data)

#     return {
#         "message": "Shipment event created",
#         "eventId": event_data["eventId"],
#         "databaseId": str(result.inserted_id)
#     }


# @router.get("/{shipment_id}")
# async def get_events(shipment_id: str):

#     events = []

#     cursor = db.shipment_events.find(
#         {"shipmentId": shipment_id}
#     ).sort("timestamp", 1)

#     async for event in cursor:
#         event["_id"] = str(event["_id"])
#         events.append(event)

#     return {
#         "count": len(events),
#         "events": events
#     }

from fastapi import APIRouter
from pydantic import BaseModel
from datetime import datetime, timezone
from app.database import db


router = APIRouter(
    prefix="/events",
    tags=["Shipment Events"]
)


class EventCreate(BaseModel):
    shipmentId: str
    vehicleId: str | None = None
    eventType: str
    description: str
    locationName: str


@router.post("/")
async def create_event(event: EventCreate):

    event_data = {
        "eventId": f"EVT-{int(datetime.now().timestamp())}",
        "shipmentId": event.shipmentId,
        "vehicleId": event.vehicleId,
        "eventType": event.eventType,
        "description": event.description,
        "locationName": event.locationName,
        "timestamp": datetime.now(timezone.utc),
        "blockchain": {
            "status": "PENDING",
            "transactionId": None
        }
    }

    try:
        result = await db.shipment_events.insert_one(event_data)

        return {
            "message": "Shipment event created",
            "eventId": event_data["eventId"],
            "databaseId": str(result.inserted_id)
        }

    except Exception:
        return {
            "message": "Shipment event created in demo mode",
            "eventId": event_data["eventId"],
            "shipmentId": event.shipmentId,
            "blockchain": {
                "status": "DEMO_PENDING",
                "transactionId": None
            }
        }


@router.get("/{shipment_id}")
async def get_events(shipment_id: str):

    events = []

    try:
        cursor = db.shipment_events.find(
            {"shipmentId": shipment_id}
        ).sort("timestamp", 1)

        async for event in cursor:
            event["_id"] = str(event["_id"])
            events.append(event)

    except Exception:
        events = [
            {
                "eventId": "EVT-001",
                "shipmentId": shipment_id,
                "vehicleId": "V001",
                "eventType": "SHIPMENT_CREATED",
                "description": "Shipment created and assigned to vehicle.",
                "locationName": "Guwahati",
                "timestamp": "2026-09-06T06:00:00Z",
                "blockchain": {
                    "status": "VERIFIED",
                    "transactionId": "DEMO-TX-001"
                }
            },
            {
                "eventId": "EVT-002",
                "shipmentId": shipment_id,
                "vehicleId": "V001",
                "eventType": "VEHICLE_DEPARTED",
                "description": "Vehicle departed from origin.",
                "locationName": "Guwahati",
                "timestamp": "2026-09-06T06:30:00Z",
                "blockchain": {
                    "status": "VERIFIED",
                    "transactionId": "DEMO-TX-002"
                }
            },
            {
                "eventId": "EVT-003",
                "shipmentId": shipment_id,
                "vehicleId": "V001",
                "eventType": "ROUTE_UPDATED",
                "description": "Safer alternative route recommended due to elevated road risk.",
                "locationName": "Shillong",
                "timestamp": "2026-09-06T08:00:00Z",
                "blockchain": {
                    "status": "VERIFIED",
                    "transactionId": "DEMO-TX-003"
                }
            }
        ]

    return {
        "count": len(events),
        "events": events
    }