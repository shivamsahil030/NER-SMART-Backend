import sys
from pathlib import Path

# Allow this script to import the backend app package when run directly.
BACKEND_DIR = Path(__file__).resolve().parents[1]
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from app.services.risk_engine import calculate_total_risk


weather = {
    "rainfallMm": 72,
    "windSpeedKmph": 38,
    "condition": "HEAVY_RAIN"
}


road = {
    "condition": "POOR",
    "riskLevel": "HIGH"
}


disruptions = [
    {
        "type": "LANDSLIDE",
        "severity": "HIGH",
        "status": "ACTIVE"
    }
]


vehicle = {
    "currentSpeedKmph": 42
}


shipment = {
    "priority": "CRITICAL"
}


result = calculate_total_risk(
    weather,
    road,
    disruptions,
    vehicle,
    shipment
)


print("\nNER-LOGIX RISK RESULT")
print("=====================")

print(
    f"Risk Score: {result['riskScore']}"
)

print(
    f"Risk Level: {result['riskLevel']}"
)

print("\nBreakdown:")

for factor, score in result["breakdown"].items():

    print(
        f"{factor}: {score}"
    )
