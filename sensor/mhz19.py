from sensor.sensorstation import Sensor, SensorData
import mh_z19


class Mhz19(Sensor):
    def measure(self) -> None:
        sensor_data = []
        co2_value = float(mh_z19.read_all()["co2"])
        sensor_data.append(SensorData(self.name, "CO2", "ppm", co2_value))
        self.sensor_data = sensor_data
