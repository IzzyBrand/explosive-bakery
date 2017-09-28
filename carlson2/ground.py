import "config.py"
import serial, struct, time

s = serial.Serial(port=port, baudrate=baud, timeout=serial_timeout)

labels = ["time","roll","pitch","yaw","altitude"]

while (True):
    bytestream = s.read(telem_data_struct_size)
    if len(bytestream) == telem_data_struct_size:
        telem_data = struct.unpack(telem_data_struct, bytestream)
        for idx, val in enumerate(telem_data):
            print labels[idx], val
        print "\n"
    time.sleep(1/telem_rate)