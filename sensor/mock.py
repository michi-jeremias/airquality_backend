from sensor.sensor import Sensor, SensorData
import random


class Mock1(Sensor):
    def measure(self) -> None:
        sensor_data = []
        sensor_data.append(
            SensorData(self.name, "CO2", "ppm", random.uniform(400.0, 1200.0))
        )
        # sensor_data.append(
        #     SensorData(self.name, "Temperature", "°C", random.uniform(22.0, 24.0))
        # )
        self.sensor_data = sensor_data


class Mock2(Sensor):
    def measure(self) -> None:
        sensor_data = []
        sensor_data.append(
            SensorData(self.name, "Humidity", "%", random.uniform(30.0, 60.0))
        )
        sensor_data.append(
            SensorData(self.name, "Temperature", "°C", random.uniform(22.0, 24.5))
        )
        self.sensor_data = sensor_data
