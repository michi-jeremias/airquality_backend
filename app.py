import eventlet
import socketio
from flask import Flask

sio = socketio.Server()
app = Flask(__name__)


@app.route("/")
def index():
    # return render_template("index.html")
    return "Flask server running!"


@sio.on("connect")
def connect(sid, environ):
    print("Client connected: ", sid)


@sio.on("data")
def data(sid, data):
    print("Received data: ", data)
    sio.emit("data", data)


if __name__ == "__main__":
    app = socketio.Middleware(sio, app)
    eventlet.wsgi.server(eventlet.listen(("", 5000)), app)
