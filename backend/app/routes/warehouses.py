# from fastapi import APIRouter
# from app.database import db


# router = APIRouter(
#     prefix="/warehouses",
#     tags=["Warehouses"]
# )


# @router.get("/")
# async def get_warehouses():

#     warehouses = []

#     async for warehouse in db.warehouses.find():
#         warehouse["_id"] = str(warehouse["_id"])
#         warehouses.append(warehouse)

#     return {
#         "count": len(warehouses),
#         "warehouses": warehouses
#     }

from fastapi import APIRouter
from app.database import db


router = APIRouter(
    prefix="/warehouses",
    tags=["Warehouses"]
)


@router.get("/")
async def get_warehouses():

    warehouses = []

    try:
        async for warehouse in db.warehouses.find():
            warehouse["_id"] = str(warehouse["_id"])
            warehouses.append(warehouse)

    except Exception:
        warehouses = [
            {
                "warehouseId": "W001",
                "name": "Guwahati Central Warehouse",
                "location": {
                    "name": "Guwahati",
                    "latitude": 26.1445,
                    "longitude": 91.7362
                },
                "capacityKg": 50000,
                "availableCapacityKg": 32000,
                "status": "OPERATIONAL"
            },
            {
                "warehouseId": "W002",
                "name": "Shillong Logistics Hub",
                "location": {
                    "name": "Shillong",
                    "latitude": 25.5788,
                    "longitude": 91.8933
                },
                "capacityKg": 30000,
                "availableCapacityKg": 18500,
                "status": "OPERATIONAL"
            },
            {
                "warehouseId": "W003",
                "name": "Itanagar Distribution Center",
                "location": {
                    "name": "Itanagar",
                    "latitude": 27.0844,
                    "longitude": 93.6053
                },
                "capacityKg": 25000,
                "availableCapacityKg": 12000,
                "status": "OPERATIONAL"
            }
        ]

    return {
        "count": len(warehouses),
        "warehouses": warehouses
    }