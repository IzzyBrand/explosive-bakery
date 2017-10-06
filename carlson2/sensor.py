# Carlson sensor class to manage sensor initialization and logging
#
# Benjamin Shanahan & Elias Berkowitz

import time

import RTIMU
from BMP280 import BMP280

RTIMU_INI_FILE = "RTIMULib"

class Sensor:

    def __init__(self):
        self.imu       = None
        self.barometer = None
        self._init_imu()
        self._init_barometer()

    def read_imu(self):
        if self.imu.IMURead():
            return imu.getIMUData()

    def read_barometer_temperature_pressure(self):
        return self.barometer.read_temperature_pressure()

    def read_barometer_altitude(self):
        return self.barometer.read_altitude()

    def _init_imu(self):
        # Configure IMU and barometer
        settings = RTIMU.Settings(RTIMU_INI_FILE)  # load calibration file
        self.imu = RTIMU.RTIMU(settings)
        if (not imu.IMUInit()):
            print "IMU failed to initialize!"
        else:
            print "IMU initialized."

        # Configure some IMU specific settings
        imu.setSlerpPower(0.02)
        imu.setGyroEnable(True)
        imu.setAccelEnable(True)
        imu.setCompassEnable(True)

    def _init_barometer(self):
        self.barometer = BMP280.BMP280()
        print "Barometer initialized."