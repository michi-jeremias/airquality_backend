import asyncio
import time
import socketio

loop = asyncio.get_event_loop()
sio = socketio.AsyncClient()
start_timer = None


@sio.event
async def connect():
    print("connected to server")


@sio.event
async def message(message: str):
    print(f"websocketclient: {sio.sid}")
    print(f"message from server: {message}")


@sio.event
async def on_data(data):
    print(f"data: {data}")
    await sio.emit("message", f"received at: {time.time()}")


async def start_server():
    await sio.connect("ws://localhost:5000", wait_timeout=10)
    await sio.wait()


if __name__ == "__main__":
    loop.run_until_complete(start_server())
