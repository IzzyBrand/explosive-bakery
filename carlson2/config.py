###############################################################################
## Sensors
###############################################################################

RTIMU_calibration_file = "RTIMULib"

###############################################################################
## Telemetry
###############################################################################

port           = "/dev/ttyUSB0"
baud           = 57600
serial_timeout = 0

###############################################################################
## Data Logging
###############################################################################

sample_rate = 50  # sample rate in Hz
telem_rate  = 5   # not Hz! Telem data is sent every 'telem_rate' samples
telem_hz    = sample_rate / telem_rate

###############################################################################
## Data structures (file save structure and telemetry structure)
###############################################################################

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