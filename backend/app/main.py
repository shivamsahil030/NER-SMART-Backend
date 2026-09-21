from contextlib import asynccontextmanager

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

from app.database import check_database_connection
from app.routes.shipments import router as shipment_router
from app.routes.vehicles import router as vehicle_router
from app.routes.gps import router as gps_router
from app.routes.weather import router as weather_router
from app.routes.roads import router as roads_router
from app.routes.disruptions import router as disruptions_router
from app.routes.alerts import router as alerts_router
from app.routes.events import router as events_router
from app.routes.routes import router as routes_router
from app.routes.warehouses import router as warehouses_router
from app.routes.risk import router as risk_router
from app.websocket import connect_client, disconnect_client
from app.routes.route_optimizer import router as route_optimizer_router
from app.routes.demo import router as demo_router




@asynccontextmanager
async def lifespan(_app: FastAPI):
    await check_database_connection()
    yield


app = FastAPI(
    title="NER-LOGIX API",
    description="AI-powered smart logistics platform for the North Eastern Region",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(shipment_router)
app.include_router(vehicle_router)
app.include_router(gps_router)
app.include_router(weather_router)
app.include_router(roads_router)
app.include_router(disruptions_router)
app.include_router(alerts_router)
app.include_router(events_router)
app.include_router(routes_router)
app.include_router(warehouses_router)
app.include_router(risk_router)
app.include_router(route_optimizer_router)
app.include_router(demo_router)




@app.get("/")
async def root():
    return {
        "message": "NER-LOGIX API is running",
        "status": "online"
    }


@app.websocket("/ws/location")
async def location_websocket(websocket: WebSocket):

    await connect_client(websocket)

    try:

        while True:
            await websocket.receive_text()

    except WebSocketDisconnect:

        disconnect_client(websocket)
