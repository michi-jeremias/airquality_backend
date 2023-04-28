from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from typing import List

import json


@dataclass
class SensorData:
    name: str
    subject: str
    unit: str
    value: float

    def encode(self) -> dict:
        return self.__dict__


class Sensor(metaclass=ABCMeta):
    def __init__(self, name: str) -> None:
        self.name: str = name
        self.sensor_data: list[SensorData] = []

    def get_sensor_data(self) -> List[SensorData]:
        return self.sensor_data

    @abstractmethod
    def measure() -> None:
        pass


class SensorStation:
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

    def get_data_json(self) -> str:
        # returns a JSON string
        data_json = json.dumps(self.get_sensor_data(), default=lambda o: o.encode())
        return data_json
