# Carlson v2
#
# This code reads the 10-DOF sensor values every 1/sample_rate seconds and
# saves them to disk. It also packs them into a C-type struct and sends them
# over telemetry to the base station (albeit at a lower data rate).
#
# Benjamin Shanahan, Elias Berkowitz, Isaiah Brand

# import sys, getopt
# sys.path.append(".")

# Import sensor libraries
import RTIMU
from BMP280 import BMP280

import serial, struct, time, math, sys

# Configure serial port where telemetry radio is connected to Carlson
port  = "/dev/ttyUSB0"
telem = serial.Serial(port=port, baudrate=57600)
print "Initialized telemetry on port %s." % port

# Additional parameters for data logging
sample_rate = 100  # sample rate in Hz
telem_rate  = 10   # not Hz! Telem data is sent every 'telem_rate' samples

t           = 0  # time stamp (sample time (sec) = t/sample_rate)

# Data structures (file save structure and telemetry structure)
#
# We use python's struct module to pack the data into a struct that we can then
# send. We pack the data so that it is smaller in transmission.
#
# file_struct = {
#     uint32_t timestamp;
#     float    roll;
#     float    pitch;
#     float    yaw;
#     float    magnetometer_x;
#     float    magnetometer_y;
#     float    magnetometer_z;
#     float    accelerometer_x;
#     float    accelerometer_y;
#     float    accelerometer_z;
#     float    gyroscope_x;
#     float    gyroscope_y;
#     float    gyroscope_z;
#     float    temperature_x;
#     float    pressure_y;
#     float    altitude_z;
# }
#
# See https://docs.python.org/2/library/struct.html
#
# I = unsigned int, 4 bytes (timestamp)
# f = float, 4 bytes (data values from sensors, see above)
file_struct      = "Ifffffffffffffff"
file_struct_size = struct.calcsize(file_struct)

# telem_data_struct = {
#     uint32_t timestamp;
#     float    roll;
#     float    pitch;
#     float    yaw;
#     float    altitude;
# }
telem_data_struct      = "Iffff"
telem_data_struct_size = struct.calcsize(telem_data_struct)


# Configure IMU and barometer
stgs = RTIMU.Settings("RTIMULib")  # load calibration file
imu  = RTIMU.RTIMU(stgs)
baro = BMP280.BMP280()

# Initialize IMU
if (not imu.IMUInit()):
    print("IMU Init Failed")
else:
    print("IMU Init Succeeded")
imu.setSlerpPower(0.02)
imu.setGyroEnable(True)
imu.setAccelEnable(True)
imu.setCompassEnable(True)

print "Carlson booted successfully."
print "Now reading sensor data!"

while (True):

    # Read data from sensors
    if imu.IMURead():
    
        # Read values from sensors and pack structure
        imu_data = imu.getIMUData()
        fusion   = imu_data["fusionPose"]
        compass  = imu_data["compass"]
        accel    = imu_data["accel"]
        gyro     = imu_data["gyro"]
        temperature, pressure = baro.read_temperature_pressure()
        altitude = baro.read_altitude()

        # # Pack file data structure
        # data = struct.pack(file_struct, t,
        #     fusion[0], fusion[1],  fusion[2],
        #     compass[0],  compass[1], compass[2],
        #     accel[0],    accel[1],   accel[2],
        #     gyro[0],     gyro[1],    gyro[2],
        #     temperature, pressure,   altitude)

        # Pack telemetry data structure and send!
        if (t % telem_rate == 0):
            telem_data = struct.pack(telem_data_struct, t, 
                math.degrees(fusion[0]), math.degrees(fusion[1]), math.degrees(fusion[2]),
                altitude)
            # Write data to telemetry radio
            telem.write(telem_data)

    # Wait a bit before taking the next sample
    time.sleep(1.0/sample_rate)
    t = t + 1;  # increment sample timestamp