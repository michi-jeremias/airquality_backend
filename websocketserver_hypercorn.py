#!/usr/bin/env python
import asyncio
from hypercorn.asyncio import serve
from hypercorn.config import Config
from datetime import datetime
import socketio

sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins="*")
app = socketio.ASGIApp(
    sio,
    static_files={
        "/": "latency.html",
        "/static": "static",
    },
)

config = Config()
config.bind = ["localhost:5000"]


@sio.event
async def connect(sid, environ, auth):
    print(f"Connected: {sid}")


@sio.event
async def disconnect(sid):
    print(f"Disconnected: {sid}")


@sio.event
async def message(sid, message: str):
    print(f"message from {sid}: {message}")


@sio.event
async def on_data(sid, data):
    now = datetime.now()
    print(f"from: {sid}")
    print(f"data: {data}")
    await sio.emit("on_data", data)
    await sio.emit("message", f"{now:%H:%M:%S}")


if __name__ == "__main__":
    asyncio.run(serve(app, config))
