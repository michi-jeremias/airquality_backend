import eventlet
import socketio
from aiohttp import web
from flask import Flask

# sio = socketio.Server()
# app = socketio.WSGIApp(sio, static_files={
#     '/': {'content_type': 'text/html', 'filename': 'index.html'}
#     })
sio = socketio.AsyncServer(async_mode="aiohttp", logger=True, engineio_logger=True)
app = web.Application()
sio.attach(app)

json_object = [
    {"name": "MH_Z19", "subject": "CO2", "unit": "ppm", "value": 567.0},
    {"name": "MH_Z19", "subject": "Temperature", "unit": " C", "value": 24.0},
    {"name": "HTU21D", "subject": "Humidity", "unit": "%", "value": 38.0},
    {"name": "HTU21D", "subject": "Temperature", "unit": " C", "value": 24.0}
    ]

@sio.on("updateMeasurements", namespace='/measurements')
async def update_measurements():
    print("Updating measurements.")
    await sio.emit('getUpdateResponse', json_object, namespace='/measurements')

# app = Flask(__name__)


# @app.route("/")
# def index():
#     # return render_template("index.html")
#     return "Flask server running!"


# @sio.on("connect")
# def connect(sid, environ):
#     print("Client connected: ", sid)

@sio.event
def connect(sid, environ):
    print("Client connected: ", sid)

@sio.event
def my_message(sid, data):
    print("message ", data)

@sio.event
def disconnect(sid):
    print("Client disconnected: ", sid)

@sio.data
def data(sid, data):
    print(f"Received data from {sid}: ", data)
    # sio.emit("data", data)

@sio.event
def get_measurements(sid, data):
    sio.emit("data", data)

if __name__ == "__main__":
    # app = socketio.Middleware(sio, app)
    # eventlet.wsgi.server(eventlet.listen(("", 5000)), app)
    web.run_app(app, port=8089)
