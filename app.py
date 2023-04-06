from abc import ABCMeta, abstractmethod
import math
from typing import List
import mh_z19
import pigpio
import time
import dataclasses
import json

from dataclasses import dataclass


@dataclass
class SensorData:
    name: str
    subject: str
    unit: str
    value: float


class Sensor(metaclass=ABCMeta):
    def __init__(self, name: str) -> None:
        self.name: str = name
        self.sensor_data: list[SensorData] = []

    def get_sensor_data(self) -> List[SensorData]:
        return self.sensor_data

    @abstractmethod
    def measure() -> None:
        pass


class Mhz19(Sensor):
    def measure(self) -> None:
        sensor_data = []
        co2_value = float(mh_z19.read_all()["co2"])
        # co2_value = 567.0
        sensor_data.append(SensorData(self.name, "CO2", "ppm", co2_value))
        # temperature_value = 24.0
        temperature_value = float(mh_z19.read_all()["temperature"])
        sensor_data.append(
            SensorData(self.name, "Temperature", " C", temperature_value)
        )
        self.sensor_data = sensor_data


class Htu21d(Sensor):
    # pi = pigpio.pi()

    # HTU21D-F Address
    addr = 0x40

    # i2c bus, if you have a Raspberry Pi Rev A, change this to 0
    bus = 1

    # HTU21D-F Commands
    rdtemp = 0xE3
    rdhumi = 0xE5
    wtreg = 0xE6
    rdreg = 0xE7
    reset = 0xFE

    @staticmethod
    def htu_reset(cls):
        handle = cls.pi.i2c_open(cls.bus, cls.addr)  # open i2c bus
        cls.pi.i2c_write_byte(handle, cls.reset)  # send reset command
        cls.pi.i2c_close(handle)  # close i2c bus
        time.sleep(0.2)  # reset takes 15ms so let's give it some time

    @staticmethod
    def read_temperature(cls):
        handle = cls.pi.i2c_open(cls.bus, cls.addr)  # open i2c bus
        cls.pi.i2c_write_byte(handle, cls.rdtemp)  # send read temp command
        time.sleep(0.055)  # readings take up to 50ms, lets give it some time
        (count, byteArray) = cls.pi.i2c_read_device(handle, 3)  # vacuum up those bytes
        cls.pi.i2c_close(handle)  # close the i2c bus
        t1 = byteArray[0]  # most significant byte msb
        t2 = byteArray[1]  # least significant byte lsb
        temp_reading = (t1 * 256) + t2  # combine both bytes into one big integer
        temp_reading = math.fabs(
            temp_reading
        )  # I'm an idiot and can't figure out any other way to make it a float
        temperature = (
            (temp_reading / 65536) * 175.72
        ) - 46.85  # formula from datasheet
        return temperature

    @staticmethod
    def read_humidity(cls):
        handle = cls.pi.i2c_open(cls.bus, cls.addr)  # open i2c bus
        cls.pi.i2c_write_byte(handle, cls.rdhumi)  # send read humi command
        time.sleep(0.055)  # readings take up to 50ms, lets give it some time
        (count, byteArray) = cls.pi.i2c_read_device(handle, 3)  # vacuum up those bytes
        cls.pi.i2c_close(handle)  # close the i2c bus
        h1 = byteArray[0]  # most significant byte msb
        h2 = byteArray[1]  # least significant byte lsb
        humi_reading = (h1 * 256) + h2  # combine both bytes into one big integer
        humi_reading = math.fabs(
            humi_reading
        )  # I'm an idiot and can't figure out any other way to make it a float
        uncomp_humidity = ((humi_reading / 65536) * 125) - 6  # formula from datasheet
        # to get the compensated humidity we need to read the temperature
        temperature = cls.read_temperature()
        humidity = ((25 - temperature) * -0.15) + uncomp_humidity
        return humidity

    def __init__(self, name: str) -> None:
        super().__init__(name)

    def measure(self) -> None:
        sensor_data = []
        humidity_value = self.read_humidity()
        sensor_data.append(SensorData(self.name, "Humidity", "%", humidity_value))
        temperature_value = self.read_temperature()
        sensor_data.append(
            SensorData(self.name, "Temperature", " C", temperature_value)
        )
        self.sensor_data = sensor_data


class SensorDataCollector:
    def __init__(self) -> None:
        self.sensors: List[Sensor] = []

    def register(self, sensor: Sensor):
        self.sensors.append(sensor)

    def measure(self):
        for sensor in self.sensors:
            sensor.measure()

    def get_sensor_data(self) -> List[SensorData]:
        sensor_data = []
        for sensor in self.sensors:
            sensor_data.extend(sensor.get_sensor_data())
        return sensor_data


if __name__ == "__main__":
    mhz19 = Mhz19("MH_Z19")
    htu21d = Htu21d("HTU21D")
    data_collector = SensorDataCollector()

    mhz19.measure()
    htu21d.measure()
    print(mhz19.get_sensor_data())
    print(htu21d.get_sensor_data())

    data_collector.register(mhz19)
    data_collector.register(htu21d)

    filepath = "data.json"
    json_string = json.dumps(
        [sensordata.__dict__ for sensordata in data_collector.get_sensor_data()]
    )
    with open(file=filepath, mode="w", encoding="utf-8") as f:
        f.write(json_string)
