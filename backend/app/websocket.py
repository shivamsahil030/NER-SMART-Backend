from fastapi import WebSocket


connected_clients: list[WebSocket] = []


async def connect_client(websocket: WebSocket):
    await websocket.accept()
    connected_clients.append(websocket)


def disconnect_client(websocket: WebSocket):
    if websocket in connected_clients:
        connected_clients.remove(websocket)


async def broadcast_location(data: dict):

    disconnected = []

    for client in connected_clients:

        try:
            await client.send_json(data)

        except Exception:
            disconnected.append(client)

    for client in disconnected:
        disconnect_client(client)