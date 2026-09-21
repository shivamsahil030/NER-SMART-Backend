# from fastapi import APIRouter
# from app.database import db


# router = APIRouter(
#     prefix="/roads",
#     tags=["Road Conditions"]
# )


# @router.get("/")
# async def get_roads():

#     roads = []

#     async for road in db.road_conditions.find():
#         road["_id"] = str(road["_id"])
#         roads.append(road)

#     return {
#         "count": len(roads),
#         "roads": roads
#     }

from fastapi import APIRouter
from app.database import db

router = APIRouter(
    prefix="/roads",
    tags=["Road Conditions"]
)


@router.get("/")
async def get_roads():

    roads = []

    try:
        async for road in db.road_conditions.find():
            road["_id"] = str(road["_id"])
            roads.append(road)

    except Exception:
        # Fallback demo road data if MongoDB is unavailable
        roads = [
            {
                "id": "nh27-gs",
                "road_id": "R001",
                "name": "NH-27 Guwahati–Shillong Corridor",
                "from": "guwahati",
                "to": "shillong",
                "status": "open",
                "risk_score": 18,
                "riskScore": 18,
                "updated": "4 min ago",
                "grade": "All-Weather",
                "incident": None,
                "passability": "Passable"
            },
            {
                "id": "nh10-sg",
                "road_id": "R002",
                "name": "NH-10 Siliguri–Gangtok (Teesta)",
                "from": "siliguri",
                "to": "gangtok",
                "status": "warning",
                "risk_score": 54,
                "riskScore": 54,
                "updated": "2 min ago",
                "grade": "Monsoon Sensitive",
                "incident": "Teesta river overflow near Sevoke — light caution",
                "passability": "Caution"
            },
            {
                "id": "nh29-dk",
                "road_id": "R003",
                "name": "NH-29 Dimapur–Kohima",
                "from": "dimapur",
                "to": "kohima",
                "status": "highrisk",
                "risk_score": 74,
                "riskScore": 74,
                "updated": "1 min ago",
                "grade": "Terrain Vulnerable",
                "incident": "Chumukedima mudslip — 78% landslide risk",
                "passability": "Restricted"
            },
            {
                "id": "nh37-gt",
                "road_id": "R004",
                "name": "NH-37 Guwahati–Tezpur",
                "from": "guwahati",
                "to": "tezpur",
                "status": "open",
                "risk_score": 22,
                "riskScore": 22,
                "updated": "6 min ago",
                "grade": "All-Weather",
                "incident": None,
                "passability": "Passable"
            },
            {
                "id": "nh715-tj",
                "road_id": "R005",
                "name": "NH-715 Tezpur–Jorhat",
                "from": "tezpur",
                "to": "jorhat",
                "status": "open",
                "risk_score": 28,
                "riskScore": 28,
                "updated": "9 min ago",
                "grade": "All-Weather",
                "incident": None,
                "passability": "Passable"
            },
            {
                "id": "nh13-ki",
                "road_id": "R006",
                "name": "NH-13 Kohima–Imphal",
                "from": "kohima",
                "to": "imphal",
                "status": "warning",
                "risk_score": 48,
                "riskScore": 48,
                "updated": "3 min ago",
                "grade": "Monsoon Sensitive",
                "incident": "Fog + intermittent rainfall advisory",
                "passability": "Caution"
            },
            {
                "id": "nh6-ss",
                "road_id": "R007",
                "name": "NH-6 Shillong–Silchar (Jaintia Hills)",
                "from": "shillong",
                "to": "silchar",
                "status": "blocked",
                "risk_score": 92,
                "riskScore": 92,
                "updated": "just now",
                "grade": "Landslide Prone",
                "incident": "Jaintia Hills landslide — 2 lanes blocked",
                "passability": "Blocked"
            },
            {
                "id": "nh6-sa",
                "road_id": "R008",
                "name": "NH-6 Silchar–Aizawl",
                "from": "silchar",
                "to": "aizawl",
                "status": "highrisk",
                "risk_score": 68,
                "riskScore": 68,
                "updated": "5 min ago",
                "grade": "Terrain Vulnerable",
                "incident": "Slope instability after heavy rain",
                "passability": "Restricted"
            },
            {
                "id": "nh8-as",
                "road_id": "R009",
                "name": "NH-08 Agartala–Silchar",
                "from": "agartala",
                "to": "silchar",
                "status": "open",
                "risk_score": 31,
                "riskScore": 31,
                "updated": "7 min ago",
                "grade": "All-Weather",
                "incident": None,
                "passability": "Passable"
            },
            {
                "id": "nh13-ti",
                "road_id": "R010",
                "name": "NH-13 Tawang–Itanagar (Sela)",
                "from": "tawang",
                "to": "itanagar",
                "status": "highrisk",
                "risk_score": 71,
                "riskScore": 71,
                "updated": "2 min ago",
                "grade": "High Altitude",
                "incident": "Sela Pass snow + fog advisory",
                "passability": "Caution"
            },
            {
                "id": "nh415-gi",
                "road_id": "R011",
                "name": "NH-415 Guwahati–Itanagar",
                "from": "guwahati",
                "to": "itanagar",
                "status": "open",
                "risk_score": 26,
                "riskScore": 26,
                "updated": "8 min ago",
                "grade": "All-Weather",
                "incident": None,
                "passability": "Passable"
            },
            {
                "id": "nh37-jd",
                "road_id": "R012",
                "name": "NH-37 Jorhat–Dibrugarh",
                "from": "jorhat",
                "to": "dibrugarh",
                "status": "open",
                "risk_score": 24,
                "riskScore": 24,
                "updated": "10 min ago",
                "grade": "All-Weather",
                "incident": None,
                "passability": "Passable"
            },
            {
                "id": "nh6-gs2",
                "road_id": "R013",
                "name": "NH-06 Guwahati–Silchar (via Meghalaya)",
                "from": "guwahati",
                "to": "silchar",
                "status": "warning",
                "risk_score": 44,
                "riskScore": 44,
                "updated": "5 min ago",
                "grade": "Monsoon Sensitive",
                "incident": "Waterlogging near Barak valley",
                "passability": "Caution"
            }
        ]

    return {
        "count": len(roads),
        "roads": roads
    }