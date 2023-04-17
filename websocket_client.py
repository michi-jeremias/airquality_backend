import asyncio
import socketio

from sensor.htu21d import Htu21d
from sensor.mhz19 import Mhz19
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
    sensorstation = SensorStation()
    sensorstation.register(Htu21d("HTU21d"))
    sensorstation.register(Mhz19("MHZ19"))

    while True:
        sensorstation.measure()
        await sio.emit("on_data", sensorstation.get_data_json())
        await sio.sleep(5)


async def start_client() -> None:
    await sio.connect("ws://localhost:5000", wait_timeout=10)
    await sio.wait()


if __name__ == "__main__":
    loop.run_until_complete(start_client())
