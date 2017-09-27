# Carlson v2
#
# This code reads the 10-DOF sensor values every 1/sample_rate seconds and
# saves them to disk. It also packs them into a C-type struct and sends them
# over telemetry to the base station (albeit at a lower data rate).
#
# Benjamin Shanahan, Elias Berkowitz, Isaiah Brand

import sys, getopt
sys.path.append(".")

import RTIMU

import serial, struct, time, math, sys

#SETTINGS_FILE = "RTIMULib"
s = RTIMU.Settings("RTIMULib")
imu = RTIMU.RTIMU(s)

# Import sensor libraries
#import RTIMU  # IMU library
#from BMP280 import BMP280  # Pressure sensor library

# Configure serial port where telemetry radio is connected to Carlson
#s = serial.Serial(port="/dev/ttyUSB0", baudrate=57600)

# Additional parameters for data logging
sample_rate = 15  # sample rate in Hz
t           = 0  # time stamp (sample time (sec) = t/sample_rate)

# Data structure sent over telemetry from Carlson to base station.
#
# We use python's struct module to pack the data into a struct that we can then
# send. We pack the data so that it is smaller in transmission.
#
# data_struct = {
#     float roll;
#     float pitch;
#     float yaw;
#     float magnetometer_x;
#     float magnetometer_y;
#     float magnetometer_z;
#     float accelerometer_x;
#     float accelerometer_y;
#     float accelerometer_z;
#     float gyroscope_x;
#     float gyroscope_y;
#     float gyroscope_z;
#     float temperature_x;
#     float pressure_y;
#     float altitude_z;
# }
#
# See https://docs.python.org/2/library/struct.html
#
# I = unsigned int, 4 bytes (timestamp)
# f = float, 4 bytes (data values from sensors, see above)
data_struct = "Ifffffffffffffff"
data_struct_size = struct.calcsize(data_struct)

# Initialize I2C sensors
#imu  = RTIMU.RTIMU(RTIMU.Settings("RTIMULib"))
print imu.IMUName()

#baro = BMP280.BMP280()

if (not imu.IMUInit()):
    print("IMU Init Failed")
else:
    print("IMU Init Succeeded")

imu.setSlerpPower(0.02)
imu.setGyroEnable(True)
imu.setAccelEnable(True)
imu.setCompassEnable(True)

while (True):

    if imu.IMURead():
    
        # Read values from sensors and pack structure
        imu_data = imu.getIMUData()
        #print imu_data
        fusion   = imu_data["fusionPose"]
        print "R",fusion[0],"P",fusion[1],"Y",fusion[2]
    # compass  = imu_data["compass"]
    # accel    = imu_data["accel"]
    # gyro     = imu_data["gyro"]
    # temperature, pressure = baro.read_temperature_pressure()
    # altitude = baro.read_altitude()

    # data = struct.pack(data_struct, t,
    #     fusion[0],   fusion[1],  fusion[2],
    #     compass[0],  compass[1], compass[2],
    #     accel[0],    accel[1],   accel[2],
    #     gyro[0],     gyro[1],    gyro[2],
    #     temperature, pressure,   altitude)
    # s.write(data)  # write data to serial

    # Wait a bit before taking the next sample
    time.sleep(1.0/sample_rate)
    t = t + 1;  # increment sample timestamp
