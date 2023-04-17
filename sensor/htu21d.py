import math
import time
import pigpio
from sensor.sensor import Sensor, SensorData


class Htu21d(Sensor):
    pi = pigpio.pi()

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
        temperature = cls.read_temperature(cls)
        humidity = ((25 - temperature) * -0.15) + uncomp_humidity
        return humidity

    def __init__(self, name: str) -> None:
        super().__init__(name)

    def measure(self) -> None:
        sensor_data = []
        humidity_value = self.read_humidity(self)
        sensor_data.append(SensorData(self.name, "Humidity", "%", humidity_value))
        # I'll be using the temperature from mhz19
        # temperature_value = self.read_temperature(self)
        # sensor_data.append(
        #     SensorData(self.name, "Temperature", "°C", temperature_value)
        # )
        self.sensor_data = sensor_data
