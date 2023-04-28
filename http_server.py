from flask import Flask, jsonify
from flask_cors import CORS
from sensor.htu21d import Htu21d
from sensor.mhz19 import Mhz19
from sensor.sensorstation import SensorStation

app = Flask(__name__)
CORS(app)

TEST_DATA = [
    {"name": "MH_Z19", "subject": "CO2", "unit": "ppm", "value": 1400.0},
    {"name": "MH_Z19", "subject": "temperature", "unit": " C", "value": 23.0},
    {"name": "HTU21D", "subject": "Humidity", "unit": "%", "value": 41.13811889648437},
]


@app.route("/")
def index():
    return "running"


@app.route("/getSensorData")
def get_sensor_data():
    # data = DATA
    sensorstation.measure()
    return sensorstation.get_data_json()


if __name__ == "__main__":
    sensorstation = SensorStation()
    sensorstation.register(Htu21d("HTU21d"))
    sensorstation.register(Mhz19("MHZ19"))
    app.run(host="0.0.0.0", port=5000, debug=True)
