from datetime import datetime, timezone

from app.database import db
from app.websocket import broadcast_location


async def create_risk_alert(
    shipment_id: str,
    vehicle_id: str | None,
    risk_result: dict
):

    risk_score = risk_result["riskScore"]
    risk_level = risk_result["riskLevel"]

    # Only create alerts for HIGH or CRITICAL risk
    if risk_score < 50:
        return None

    # Prevent duplicate active alerts
    existing_alert = await db.alerts.find_one({
        "shipmentId": shipment_id,
        "type": "ROUTE_RISK",
        "status": "ACTIVE"
    })

    if existing_alert:
        return {
            "message": "Active risk alert already exists",
            "alertId": str(existing_alert["_id"])
        }

    if risk_level == "CRITICAL":
        severity = "CRITICAL"
    else:
        severity = "HIGH"

    alert = {
        "alertId": f"RISK-{int(datetime.now().timestamp())}",
        "type": "ROUTE_RISK",
        "severity": severity,
        "title": f"{risk_level} route risk detected",
        "message": (
            f"Shipment {shipment_id} has a route risk "
            f"score of {risk_score}/100."
        ),
        "shipmentId": shipment_id,
        "vehicleId": vehicle_id,
        "riskScore": risk_score,
        "riskBreakdown": risk_result["breakdown"],
        "status": "ACTIVE",
        "source": "RISK_ENGINE",
        "createdAt": datetime.now(timezone.utc),
        "resolvedAt": None
    }

    await db.alerts.insert_one(alert)

    # Send alert to connected clients
    await broadcast_location({
        "type": "ALERT",
        "alertId": alert["alertId"],
        "shipmentId": shipment_id,
        "vehicleId": vehicle_id,
        "severity": severity,
        "riskScore": risk_score,
        "message": alert["message"]
    })

    return alert