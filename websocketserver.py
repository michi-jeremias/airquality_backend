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


# @sio.event
# async def datarequest_from_frontend(sid):
#     print("Data received from frontend")
#     await sio.emit("getSensorData")


@sio.event
async def message(sid, message: str):
    print(f"message from {sid}: {message}")


@sio.event
async def on_data(sid, data):
    print(f"from: {sid}")
    print(f"data: {data}")
    await sio.emit("message", f"received at: {time.time()}")


# json_object = [
#     {"name": "MH_Z19", "subject": "CO2", "unit": "ppm", "value": 567.0},
#     {"name": "MH_Z19", "subject": "Temperature", "unit": " C", "value": 24.0},
#     {"name": "HTU21D", "subject": "Humidity", "unit": "%", "value": 38.0},
#     {"name": "HTU21D", "subject": "Temperature", "unit": " C", "value": 24.0},
# ]

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=5000)

    # while True:
    #     sensordata()
    #     asyncio.sleep(2)
