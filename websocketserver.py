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
async def message(sid, message: str):
    print(f"message from {sid}: {message}")


@sio.event
async def on_data(sid, data):
    print(f"from: {sid}")
    print(f"data: {data}")
    await sio.emit("on_data", data)
    await sio.emit("message", f"received at: {time.time()}")
    await sio.emit("message2", f"msg 2 received at: {time.time()}")


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=5000)
