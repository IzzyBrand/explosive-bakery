import serial, struct, time

s = serial.Serial(port="/dev/ttyUSB0", baudrate=57600, timeout=0)

telem_rate  = 10  # telemetry read rate in Hz
t           = 0  # time stamp (sample time (sec) = t/sample_rate)

telem_data_struct      = "Iffff"
telem_data_struct_size = struct.calcsize(telem_data_struct)

labels = ["time","roll","pitch","yaw","altitude"]

while (True):
    bytestream = s.read(telem_data_struct_size)
    if len(bytestream) == telem_data_struct_size:
        telem_data = struct.unpack(telem_data_struct, bytestream)
        for idx, val in enumerate(telem_data):
            print labels[idx], val
        print "\n"
    time.sleep(1/telem_rate)