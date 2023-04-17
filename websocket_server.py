#!/usr/bin/env python
import asyncio
from hypercorn.asyncio import serve
from hypercorn.config import Config
from datetime import datetime
import socketio

sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins="*")
app = socketio.ASGIApp(sio)

config = Config()
config.bind = ["localhost:5000"]


@sio.event
async def connect(sid: str, environ, auth) -> None:
    print(f"Connected: sid: {sid}")


@sio.event
async def disconnect(sid: str) -> None:
    print(f"Disconnected: {sid}")


@sio.event
async def message(message: str) -> None:
    print(f"{message}")


@sio.event
async def on_data(sid: str, data: str) -> None:
    now = datetime.now()
    print(f"Message from: {sid}")
    await sio.emit("on_data", data)
    await sio.emit("message", f"Message received: {now:%H:%M:%S}")


if __name__ == "__main__":
    asyncio.run(serve(app, config))
