#!/usr/bin/env python
import asyncio
from python_json_config import ConfigBuilder
from hypercorn.asyncio import serve
from hypercorn.config import Config
from datetime import datetime
import socketio

sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins="*")
app = socketio.ASGIApp(sio)


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
    config = Config()
    builder = ConfigBuilder()
    json_config = builder.parse_config("config.json")
    host = json_config.server.host
    port = json_config.server.port
    config.bind = [f"{host}:{port}"]

    asyncio.run(serve(app, config))
