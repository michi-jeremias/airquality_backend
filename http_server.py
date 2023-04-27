from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

data = [
    {"name": "MH_Z19", "subject": "CO2", "unit": "ppm", "value": 1400.0},
    {"name": "MH_Z19", "subject": "temperature", "unit": " C", "value": 23.0},
    {"name": "HTU21D", "subject": "Humidity", "unit": "%", "value": 41.13811889648437},
]


@app.route("/")
def index():
    return "running"


@app.route("/getSensorData")
def get_sensor_data():
    return jsonify(data)


if __name__ == "__main__":
    app.run(host="192.168.100.12", port=5000, debug=True)
