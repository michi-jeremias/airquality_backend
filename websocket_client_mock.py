import asyncio
import socketio

from sensor.mock import Mock1, Mock2
from sensor.sensor import SensorStation


loop = asyncio.get_event_loop()
sio = socketio.AsyncClient()


@sio.event
async def connect() -> None:
    print(f"Connected with id: {sio.sid}")
    await measure_and_send()


@sio.event
async def message(message: str) -> None:
    print(f"{message}")


async def measure_and_send() -> None:
    datastation = SensorStation()
    datastation.register(Mock1("Mock1"))
    datastation.register(Mock2("Mock2"))

    while True:
        datastation.measure()
        await sio.emit("on_data", datastation.get_data_json())
        await sio.sleep(5)


async def start_client() -> None:
    await sio.connect("ws://localhost:5000", wait_timeout=10)
    await sio.wait()


if __name__ == "__main__":
    loop.run_until_complete(start_client())
