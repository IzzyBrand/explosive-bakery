# Carlson v2
#
# This code reads the 10-DOF sensor values every 1/sample_rate seconds and
# saves them to disk. It also packs them into a C-type struct and sends them
# over telemetry to the base station (albeit at a lower data rate).
#
# Benjamin Shanahan, Elias Berkowitz, Isaiah Brand

# import sys, getopt
# sys.path.append(".")

import config

# Import sensor libraries
import RTIMU
from BMP280 import BMP280

import serial, struct, time, math, sys, os

# Configure serial port where telemetry radio is connected to Carlson
telem = serial.Serial(port=config.port, baudrate=config.baud, timeout=config.serial_timeout)
print "Initialized telemetry on port %s at baud %d." % (config.port, config.baud)

while (True):

    # Read incoming command over telemetry
    command = telem.read(1)
    if command != "":
        print "!!! received:", command
        if command == "a":
            print "ARMED"
        elif command == "d":
            print "DEPLOYED CHUTE"
        elif command == "x":
            print "STOPPED DATA LOGGING"
        else:
            print "UNRECOGNIZED COMMAND"
        telem.write(command)

    # Wait a bit before taking the next sample
    time.sleep(1.0/config.sample_rate)
    # t = t + 1  # increment sample timestamp

