import asyncio
import time
import socketio

loop = asyncio.get_event_loop()
sio = socketio.AsyncClient()
start_timer = None


# async def send_ping():
#     global start_timer
#     start_timer = time.time()
#     await sio.emit("ping_from_client")


@sio.event
async def connect():
    print("connected to server")
    # await send_message("first message hiho")


@sio.event
async def message(message: str):
    print(f"websocketclient: {sio.sid}")
    print(f"message from server: {message}")
    # await sio.emit("request_message", time.time())


async def start_server():
    await sio.connect("ws://localhost:5000", wait_timeout=10)
    await sio.wait()


if __name__ == "__main__":
    loop.run_until_complete(start_server())
