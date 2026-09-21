# from datetime import datetime, timezone

# from app.database import db


# async def activate_landslide_scenario(
#     shipment_id: str
# ):

#     now = datetime.now(timezone.utc)

#     disruption = {
#         "disruptionId": f"DEMO-LANDSLIDE-{int(now.timestamp())}",
#         "type": "LANDSLIDE",
#         "severity": "CRITICAL",
#         "status": "ACTIVE",
#         "title": "Major Landslide Detected",
#         "description": (
#             "Landslide reported on the active shipment corridor."
#         ),
#         "affectedRoad": "NH-15",
#         "latitude": 26.82,
#         "longitude": 92.42,
#         "reportedAt": now,
#         "source": "DEMO_SIMULATION"
#     }

#     insert_result = await db.disruptions.insert_one(disruption)

#     await db.shipments.update_one(
#         {"shipmentId": shipment_id},
#         {
#             "$set": {
#                 "status": "AT_RISK",
#                 "riskStatus": "DISRUPTION_DETECTED"
#             }
#         }
#     )

#     return {
#         "message": "Landslide scenario activated",
#         "shipmentId": shipment_id,
#         "disruption": {
#             **disruption,
#             "_id": str(insert_result.inserted_id)
#         }
#     }

from datetime import datetime, timezone

from app.database import db


async def activate_landslide_scenario(shipment_id: str):

    now = datetime.now(timezone.utc)

    disruption = {
        "disruptionId": f"DEMO-LANDSLIDE-{int(now.timestamp())}",
        "type": "LANDSLIDE",
        "severity": "CRITICAL",
        "status": "ACTIVE",
        "title": "Major Landslide Detected",
        "description": (
            "Landslide reported on the active shipment corridor."
        ),
        "affectedRoad": "NH-15",
        "latitude": 26.82,
        "longitude": 92.42,
        "reportedAt": now,
        "source": "DEMO_SIMULATION"
    }

    try:
        insert_result = await db.disruptions.insert_one(disruption)

        await db.shipments.update_one(
            {"shipmentId": shipment_id},
            {
                "$set": {
                    "status": "AT_RISK",
                    "riskStatus": "DISRUPTION_DETECTED"
                }
            }
        )

        return {
            "message": "Landslide scenario activated",
            "mode": "DATABASE",
            "shipmentId": shipment_id,
            "disruption": {
                **disruption,
                "_id": str(insert_result.inserted_id)
            }
        }

    except Exception:

        return {
            "message": "Landslide scenario activated",
            "mode": "DEMO",
            "shipmentId": shipment_id,
            "disruption": {
                **disruption,
                "reportedAt": now.isoformat(),
                "_id": "DEMO-LANDSLIDE"
            },
            "shipment": {
                "status": "AT_RISK",
                "riskStatus": "DISRUPTION_DETECTED"
            }
        }