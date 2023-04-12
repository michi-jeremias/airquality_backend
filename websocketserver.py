#!/usr/bin/env python
import uvicorn
import time
import socketio
import asyncio

sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins="*")
app = socketio.ASGIApp(
    sio,
    static_files={
        "/": "latency.html",
        "/static": "static",
    },
)


@sio.event
async def connect(sid, environ, auth):
    print(f"Connected: {sid}")


@sio.event
async def disconnect(sid):
    print(f"Disconnected: {sid}")


@sio.event
async def ping_from_client(sid):
    await sio.emit("pong_from_server", room=sid)


@sio.event
async def datarequest_from_frontend(sid):
    print("Data received from frontend")
    await sio.emit("getSensorData")


@sio.event
async def sensordata():
    await sio.emit("huhu got it")
    print("emitted")
    # await sio.emit(json_object)


json_object = [
    {"name": "MH_Z19", "subject": "CO2", "unit": "ppm", "value": 567.0},
    {"name": "MH_Z19", "subject": "Temperature", "unit": " C", "value": 24.0},
    {"name": "HTU21D", "subject": "Humidity", "unit": "%", "value": 38.0},
    {"name": "HTU21D", "subject": "Temperature", "unit": " C", "value": 24.0},
]

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=5000)

    while True:
        sensordata()
        asyncio.sleep(2)
