import serial, struct

s = serial.Serial(port="/dev/ttyUSB0", baudrate=57600, timeout=60)

sample_rate = 100  # sample rate in Hz
t           = 0  # time stamp (sample time (sec) = t/sample_rate)

telem_data_struct      = "Iffff"
telem_data_struct_size = struct.calcsize(telem_data_struct)

labels = ["time","roll","pitch","yaw","altitude"]

while (True):
    bytestream = s.read(telem_data_struct_size)
    telem_data = struct.unpack(telem_data_struct, bytestream)
    for idx, val in enumerate(telem_data):
        print labels[idx], val
    print "\n"