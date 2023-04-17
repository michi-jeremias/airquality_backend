import asyncio
import socketio

import mocksensors
from sensor import SensorDataCollector


loop = asyncio.get_event_loop()
sio = socketio.AsyncClient()


@sio.event
async def connect() -> None:
    await measure_and_send()


@sio.event
async def message(message: str) -> None:
    print(f"websocketclient: {sio.sid}")
    print(f"message from server: {message}")


async def measure_and_send() -> None:
    datastation = SensorDataCollector()
    datastation.register(mocksensors.Mock1("Mock CO2 Temp"))
    datastation.register(mocksensors.Mock1("Mock2 CO2 Temp"))
    datastation.register(mocksensors.Mock2("Mock Temp Hum"))

    while True:
        datastation.measure()
        await sio.emit("on_data", datastation.get_data_json())
        await sio.sleep(4)


async def start_client() -> None:
    await sio.connect("ws://localhost:5000", wait_timeout=10)
    await sio.wait()


if __name__ == "__main__":
    loop.run_until_complete(start_client())
