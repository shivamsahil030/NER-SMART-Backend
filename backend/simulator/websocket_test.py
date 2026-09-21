import asyncio
import websockets


async def test():

    uri = "ws://127.0.0.1:8000/ws/location"

    async with websockets.connect(uri) as websocket:

        print("Connected to NER-LOGIX WebSocket")

        while True:

            message = await websocket.recv()

            print("GPS UPDATE:", message)


asyncio.run(test())