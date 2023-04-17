import asyncio
import json
import socketio

loop = asyncio.get_event_loop()
sio = socketio.AsyncClient()


class SensorData(dict):
    def __init__(self, name: str, subject: str, unit: str, value: float) -> None:
        dict.__init__(self, name=name, subject=subject, unit=unit, value=value)

    def encode(self) -> dict:
        return self.__dict__


@sio.event
async def connect() -> None:
    await send_data()


@sio.event
async def on_data(sid: str, data: str) -> None:
    print(f"from: {sid}")
    print(f"data: {data}")


@sio.event
async def message(message: str) -> None:
    print(f"websocketclient: {sio.sid}")
    print(f"message from server: {message}")


async def send_data() -> None:
    sensor_data = [
        SensorData("MH_Z19", "CO2", "ppm", 500.0),
        SensorData("MH_Z19", "Temperature", " C", 20.0),
    ]
    sensor_data_json = json.dumps(sensor_data, default=lambda o: o.encode())
    while True:
        await sio.emit("on_data", sensor_data_json)
        await sio.sleep(4)


async def start_client() -> None:
    await sio.connect("ws://localhost:5000", wait_timeout=10)
    await sio.wait()


if __name__ == "__main__":
    loop.run_until_complete(start_client())
