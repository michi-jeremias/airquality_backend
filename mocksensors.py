from mocksensors import Sensor, SensorData


class Mock1(Sensor):
    def measure(self) -> None:
        sensor_data = []
        sensor_data.append(SensorData(self.name, "CO2", "ppm", 528))
        sensor_data.append(SensorData(self.name, "Temperature", " C", 24.0))
        self.sensor_data = sensor_data


class Mock2(Sensor):
    def measure(self) -> None:
        sensor_data = []
        sensor_data.append(SensorData(self.name, "Humidity", "%", 45.0))
        sensor_data.append(SensorData(self.name, "Temperature", " C", 23.5))
        self.sensor_data = sensor_data
