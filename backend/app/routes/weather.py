# from fastapi import APIRouter
# from app.database import db


# router = APIRouter(
#     prefix="/weather",
#     tags=["Weather"]
# )


# @router.get("/")
# async def get_weather():

#     weather = []

#     async for item in db.weather_data.find().sort("timestamp", -1):
#         item["_id"] = str(item["_id"])
#         weather.append(item)

#     return {
#         "count": len(weather),
#         "weather": weather
#     }

from fastapi import APIRouter
from app.database import db

router = APIRouter(
    prefix="/weather",
    tags=["Weather"]
)

@router.get("/")
async def get_weather():

    weather = []

    try:
        async for item in db.weather_data.find().sort("timestamp", -1):
            item["_id"] = str(item["_id"])
            weather.append(item)

    except Exception:
        # Fallback demo data if MongoDB is unavailable
        weather = [
            {
                "location": "Guwahati",
                "temperature": 24,
                "humidity": 88,
                "rainfall": 12,
                "wind": 14,
                "condition": "Heavy Rain",
                "warning": "Monsoon Alert Level 3"
            },
            {
                "location": "Shillong",
                "temperature": 20,
                "humidity": 91,
                "rainfall": 18,
                "wind": 11,
                "condition": "Rain",
                "warning": "Landslide Risk"
            }
        ]

    return {
        "count": len(weather),
        "weather": weather
    }