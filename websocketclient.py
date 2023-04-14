import asyncio
import json
import socketio

loop = asyncio.get_event_loop()
sio = socketio.AsyncClient()
start_timer = None


class SensorData(dict):
    def __init__(self, name, subject, unit, value):
        dict.__init__(self, name=name, subject=subject, unit=unit, value=value)

    def encode(self):
        return self.__dict__


@sio.event
async def connect():
    await send_data()


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
    json_object = [
        {"name": "MH_Z19", "subject": "CO2", "unit": "ppm", "value": 567.0},
        {
            "name": "MH_Z19",
            "subject": "Temperature",
            "unit": " C",
            "value": 24.0,
        },
        {"name": "MH_Z19", "subject": "Temperature", "unit": " C", "value": 24.0},
        {
            "name": "HTU21D",
            "subject": "Temperature",
            "unit": " C",
            "value": 24.0,
        },
        {"name": "HTU21D", "subject": "Humidity", "unit": "%", "value": 38.0},
    ]

    json_data = [
        SensorData("MH_Z19", "CO2", "ppm", 567.0),
        SensorData("MH_Z19", "Temperature", " C", 24.0),
    ]
    jjson = json.dumps(json_data, default=lambda o: o.encode())  # .replace('"', "'")
    while True:
        await sio.emit("on_data", jjson)
        await sio.sleep(4)


async def start_client():
    await sio.connect("ws://localhost:5000", wait_timeout=10)
    await sio.wait()


if __name__ == "__main__":
    loop.run_until_complete(start_client())
