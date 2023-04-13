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
    await send_data()


# @sio.event
# async def send_message(message: str):
#     print(f"emitting message: {message}")
#     await sio.emit("message", message)


# @sio.event
# async def request_message(time: str):
#     message: str = "triggered message"
#     print(f"trigger new message: {message}: {time}")
#     await sio.sleep(1)
#     if sio.connected:
#         await send_message(message)


@sio.event
async def on_data(sid, data):
    print(f"from: {sid}")
    print(f"data: {data}")


@sio.event
async def message(message: str):
    print(f"websocketclient: {sio.sid}")
    print(f"message from server: {message}")
    # await sio.emit("request_message", time.time())


async def send_data():
    while True:
        await sio.emit("on_data", {"foo": "bar"})
        await sio.sleep(4)


# @sio.event
# async def pong_from_server():
#     global start_timer
#     latency = time.time() - start_timer
#     print("latency is {0:.2f} ms".format(latency * 1000))
#     await sio.sleep(1)
#     if sio.connected:
#         await send_ping()


async def start_server():
    await sio.connect("ws://localhost:5000", wait_timeout=10)
    await sio.wait()


if __name__ == "__main__":
    loop.run_until_complete(start_server())
