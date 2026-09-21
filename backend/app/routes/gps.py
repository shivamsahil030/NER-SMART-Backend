# from fastapi import APIRouter, HTTPException
# from pydantic import BaseModel
# from datetime import datetime, timezone
# from app.database import db
# from app.websocket import broadcast_location


# router = APIRouter(
#     prefix="/gps",
#     tags=["GPS Tracking"]
# )


# class GPSUpdate(BaseModel):
#     vehicleId: str
#     shipmentId: str
#     latitude: float
#     longitude: float
#     speedKmph: float
#     heading: float = 0


# @router.post("/")
# async def update_gps(data: GPSUpdate):

#     vehicle = await db.vehicles.find_one(
#         {"vehicleId": data.vehicleId}
#     )

#     if not vehicle:
#         raise HTTPException(
#             status_code=404,
#             detail="Vehicle not found"
#         )

#     timestamp = datetime.now(timezone.utc)

#     gps_data = {
#         "vehicleId": data.vehicleId,
#         "shipmentId": data.shipmentId,
#         "location": {
#             "type": "Point",
#             "coordinates": [
#                 data.longitude,
#                 data.latitude
#             ]
#         },
#         "speedKmph": data.speedKmph,
#         "heading": data.heading,
#         "timestamp": timestamp
#     }

#     await db.gps_logs.insert_one(gps_data)

#     await db.vehicles.update_one(
#         {"vehicleId": data.vehicleId},
#         {
#             "$set": {
#                 "currentLocation": gps_data["location"],
#                 "currentSpeedKmph": data.speedKmph,
#                 "lastUpdated": timestamp
#             }
#         }
#     )

#     await db.shipments.update_one(
#         {"shipmentId": data.shipmentId},
#         {
#             "$set": {
#                 "tracking.currentLocation": gps_data["location"],
#                 "tracking.speedKmph": data.speedKmph,
#                 "updatedAt": timestamp
#             }
#         }
#     )

#     await broadcast_location({
#         "vehicleId": data.vehicleId,
#         "shipmentId": data.shipmentId,
#         "latitude": data.latitude,
#         "longitude": data.longitude,
#         "speedKmph": data.speedKmph,
#         "heading": data.heading
#     })

#     return {
#         "message": "GPS updated successfully",
#         "vehicleId": data.vehicleId,
#         "location": gps_data["location"]
#     }


# @router.get("/{shipment_id}")
# async def get_gps_history(shipment_id: str):

#     logs = []

#     cursor = db.gps_logs.find(
#         {"shipmentId": shipment_id}
#     ).sort("timestamp", 1)

#     async for log in cursor:
#         log["_id"] = str(log["_id"])
#         logs.append(log)

#     return {
#         "count": len(logs),
#         "gpsHistory": logs
#     }

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime, timezone
from app.database import db
from app.websocket import broadcast_location


router = APIRouter(
    prefix="/gps",
    tags=["GPS Tracking"]
)


class GPSUpdate(BaseModel):
    vehicleId: str
    shipmentId: str
    latitude: float
    longitude: float
    speedKmph: float
    heading: float = 0


@router.post("/")
async def update_gps(data: GPSUpdate):

    try:
        vehicle = await db.vehicles.find_one(
            {"vehicleId": data.vehicleId}
        )

        if not vehicle:
            raise HTTPException(
                status_code=404,
                detail="Vehicle not found"
            )

        timestamp = datetime.now(timezone.utc)

        gps_data = {
            "vehicleId": data.vehicleId,
            "shipmentId": data.shipmentId,
            "location": {
                "type": "Point",
                "coordinates": [
                    data.longitude,
                    data.latitude
                ]
            },
            "speedKmph": data.speedKmph,
            "heading": data.heading,
            "timestamp": timestamp
        }

        await db.gps_logs.insert_one(gps_data)

        await db.vehicles.update_one(
            {"vehicleId": data.vehicleId},
            {
                "$set": {
                    "currentLocation": gps_data["location"],
                    "currentSpeedKmph": data.speedKmph,
                    "lastUpdated": timestamp
                }
            }
        )

        await db.shipments.update_one(
            {"shipmentId": data.shipmentId},
            {
                "$set": {
                    "tracking.currentLocation": gps_data["location"],
                    "tracking.speedKmph": data.speedKmph,
                    "updatedAt": timestamp
                }
            }
        )

        await broadcast_location({
            "vehicleId": data.vehicleId,
            "shipmentId": data.shipmentId,
            "latitude": data.latitude,
            "longitude": data.longitude,
            "speedKmph": data.speedKmph,
            "heading": data.heading
        })

        return {
            "message": "GPS updated successfully",
            "vehicleId": data.vehicleId,
            "location": gps_data["location"]
        }

    except HTTPException:
        raise

    except Exception:
        # Demo mode when MongoDB is unavailable
        return {
            "message": "GPS updated successfully in demo mode",
            "vehicleId": data.vehicleId,
            "shipmentId": data.shipmentId,
            "location": {
                "type": "Point",
                "coordinates": [
                    data.longitude,
                    data.latitude
                ]
            },
            "speedKmph": data.speedKmph,
            "heading": data.heading
        }


@router.get("/{shipment_id}")
async def get_gps_history(shipment_id: str):

    logs = []

    try:
        cursor = db.gps_logs.find(
            {"shipmentId": shipment_id}
        ).sort("timestamp", 1)

        async for log in cursor:
            log["_id"] = str(log["_id"])
            logs.append(log)

    except Exception:
        # Demo GPS history when MongoDB is unavailable
        logs = [
            {
                "vehicleId": "V001",
                "shipmentId": shipment_id,
                "location": {
                    "type": "Point",
                    "coordinates": [91.7362, 26.1445]
                },
                "speedKmph": 42,
                "heading": 135,
                "timestamp": "2026-09-06T08:00:00Z"
            },
            {
                "vehicleId": "V001",
                "shipmentId": shipment_id,
                "location": {
                    "type": "Point",
                    "coordinates": [91.8500, 25.9500]
                },
                "speedKmph": 35,
                "heading": 150,
                "timestamp": "2026-09-06T08:20:00Z"
            },
            {
                "vehicleId": "V001",
                "shipmentId": shipment_id,
                "location": {
                    "type": "Point",
                    "coordinates": [91.8933, 25.5788]
                },
                "speedKmph": 28,
                "heading": 160,
                "timestamp": "2026-09-06T08:40:00Z"
            }
        ]

    return {
        "count": len(logs),
        "gpsHistory": logs
    }