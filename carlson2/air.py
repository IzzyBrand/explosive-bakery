#!/usr/bin/python

# Carlson v2
#
# This code reads the 10-DOF sensor values every 1/sample_rate seconds and
# saves them to disk. It also packs them into a C-type struct and sends them
# over telemetry to the base station (albeit at a lower data rate).
#
# Benjamin Shanahan, Elias Berkowitz, Isaiah Brand

import config
import RPi.GPIO as GPIO
# Import sensor libraries
import RTIMU
from BMP280 import BMP280

import serial, struct, time, math, sys, os
from datetime import datetime as dt

# Configure serial port where telemetry radio is connected to Carlson
i = 0
while True:
    try:
        telem = serial.Serial(port=config.port,
                              baudrate=config.baud,
                              timeout=config.serial_timeout)
        break
    except serial.serialutil.SerialException:
        i += 1
        time.sleep(.5)

print "Initialized telemetry on port %s at baud %d." % (config.port, config.baud)

## Create new logging file
script_path = os.path.abspath(os.path.expanduser(sys.argv[0]))
folder = os.path.split(script_path)[0]
log_folder = '%s/%s' % (folder, config.log_folder)

last_launch = 0

for f in [x for x in os.listdir(log_folder) if x.endswith('.csv')]:
    try:
        launch_numb = int(f.split('_')[0])
        last_launch = launch_numb if launch_numb > last_launch else last_launch
    except ValueError:
        print 'Warning: Invalid csv file in logs folder (%s)' % f

date_str = dt.now().strftime('%y-%m-%d')

if last_launch + 1 < 10:
    filename = '0%s_%s' % (last_launch + 1, date_str)
else:
    filename = '%s_%s' % (last_launch + 1, date_str)

LOG_PATH = '%s/%s.csv' % (log_folder, filename)
if os.path.exists(LOG_PATH):
    print 'ERROR: Log file already exists (%s)' % LOG_PATH
    print 'This is probably a code error'
    sys.exit(0)

LOG_FILE = open('%s/%s.csv' % (log_folder, filename), 'a')
## End logging file finding/opening

# GPIO setup
GPIO.setmode(GPIO.BCM) # Broadcom pin-numbering scheme
GPIO.setup(config.chute_pin, GPIO.OUT) # LED pin set as output
GPIO.output(config.chute_pin, GPIO.LOW)

# Configure IMU and barometer
stgs = RTIMU.Settings(config.RTIMU_calibration_file)  # load calibration file
imu  = RTIMU.RTIMU(stgs)
baro = BMP280.BMP280()
print "BMP280 init succeeded"

# Initialize IMU
if (not imu.IMUInit()):
    print "IMU init failed"
else:
    print "IMU init succeeded"

imu.setSlerpPower(0.02)
imu.setGyroEnable(True)
imu.setAccelEnable(True)
imu.setCompassEnable(True)

t               = 0   # time stamp (sample time (sec) = t/sample_rate)
current_command = ""  # stores last unique command received by rocket

print "Carlson booted successfully. Waiting for arm command."

# Stop Carlson and send heartbeats infinitely until we receive the arm command,
# which will tell Carlson to break from the heartbeat loop and start logging
# data.
while (True):
    telem.write(config.HEARTBEAT)
    command = telem.read(1)
    if command == config.ARM:
        print "ARMED"
        telem.write(command)  # respond to ground station
        break;  # go into armed state
    time.sleep(config.heartbeat_delay)

print "Reading sensor data at %.2f Hz and sending telemetry updates at %.2f Hz!" % (config.sample_rate, config.telem_hz)

# Armed state, data logging enabled.
t0 = time.time()  # get initial time so we can subtract it
deployed_chute = False
while (True):

    # Read incoming command over telemetry
    command = telem.read(1)
    if command != "" and command != current_command:
        current_command = command
        if command == config.DEPLOY:
            
	    GPIO.output(config.chute_pin, GPIO.HIGH)
	    chute_time = time.time()
	    deployed_chute = True
            print "DEPLOYED CHUTE"
            telem.write(command)
        elif deployed_chute and command == config.STOP:
            print "STOPPED DATA LOGGING"
            telem.write(command)  # do this because we break
            break;
        elif command == config.ARM:
            print "ROCKET ALREADY ARMED"
            telem.write(command)
        else:
            print "UNRECOGNIZED COMMAND"
            telem.write(config.NOPE)
    
    if deployed_chute and GPIO.input(config.chute_pin) and time.time() - chute_time > config.blast_cap_burn_time:
	GPIO.output(config.chute_pin, GPIO.LOW)

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

        # Pack file data structure
        data = [time.time()-t0, 
                fusion[0],   fusion[1],  fusion[2],  # roll, pitch, yaw in default sensor orientation
                compass[0],  compass[1], compass[2],
                accel[0],    accel[1],   accel[2],
                gyro[0],     gyro[1],    gyro[2],
                temperature, pressure,   altitude,
                current_command]
        n_data = 17  # hard-coded cuz faster

        # Log current data to a csv
        log_str = ""
        for idx, datum in enumerate(data):
            log_str += "%s" % datum
            if idx == n_data-1:
                log_str += "\n"
            else:
                log_str += ","

        # Log data to and flush file
        LOG_FILE.write(log_str)
        LOG_FILE.flush()

    # Wait a bit before taking the next sample
    time.sleep(1.0/config.sample_rate)

print "Carlson shut down."
