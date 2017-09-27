import serial, struct

s = serial.Serial(port="/dev/ttyUSB0", baudrate=57600, timeout=60)

sample_rate = 4  # sample rate in Hz
t           = 0  # time stamp (sample time (sec) = t/sample_rate)

data_struct = "Ifffffffffffffff"
data_struct_size = struct.calcsize(data_struct)

labels = [
        "time",
        "roll","pitch","yaw",
        "compass_x","compass_y","compass_z",
        "accel_x","accel_y","accel_z",
        "gyro_x","gyro_y","gyro_z",
        "temp","pressure","altitude"]

while (True):
    bytestream = s.read(data_struct_size)
    data = struct.unpack(data_struct, bytestream)
    for idx, val in enumerate(data):
        print labels[idx], val
    print "\n\n\n\n"