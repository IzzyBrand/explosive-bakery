#!/usr/bin/python

# Carlson AIR station v0.3
#
# 5 October 2017, Benjamin Shanahan.

import time
import serial
import os

import logger as lgr
import wirelesscommunicator as wc
from state import State
from telemetry import Telemetry
from sensor import Sensor
from gpio import Pin

HEARTBEAT_DELAY = 1  # seconds, how often do we send state to ground station
BLAST_CAP_BURN_TIME = 5  # seconds, how long to keep relay shorted for

# Should we debug?
LOG_DEBUG = True  # Save debug info to a local text file
# TODO: **important** THIS OPTION (UDP_DEBUG) SHOULD BE FALSE UNLESS MANUALLY SPECIFIED BY A FLAG (ARGPARSER)
UDP_DEBUG = True  # Send info across network to another machine on the network

if __name__ == "__main__":

    # Bit latches
    arm             = False
    logging         = False
    deploy_chute    = False
    power_off       = False

    # Current state latches
    _armed          = False
    _logging_on     = False
    _chute_deployed = False

    # Set current state of air controller and declare the time we last sent a 
    # state update to the ground station
    state           = State()
    state_last_sent = 0

    # Timing variables
    time_chute_deployed = 0

    ###########################################################################
    ## Initialize Wireless Communication
    ###########################################################################

    # TODO: allow IPs and ports to be specified via argparser
    if UDP_DEBUG:
        host_port   = 5000             # Carlson's port (local)
        target_ip   = "192.168.1.228"  # IP of laptop running WIFIDEBUGGER
        target_port = 5001             # Port on laptop running WIFIDEBUGGER
        wifidebugger = wc.WirelessCommunicator(
            host_port=host_port, target_ip=target_ip, target_port=target_port)

    ###########################################################################
    ## Initialize our external devices
    ###########################################################################

    # Define logger but don't initialize a new log file here
    logger = lgr.Logger(init_log=False, init_camera=False, init_debug=True)

    # Define debug function
    def debug(text):
        if LOG_DEBUG: logger.write(text, lgr.DEBUG)

    # Initialize telemetry radio for communication with ground station
    radio = Telemetry()
    debug("Initialized telemetry.")

    # Initialize the IMU and barometer sensors so that we can read from them
    sensor = Sensor()
    debug("Initialized sensor.")

    # Initialize the GPIO pins so that we can write them high or low
    chute_pin = Pin(4)
    debug("Initialized chute pin.")

    # Main loop
    t0 = 0
    debug("Entering program loop.")
    while (True):

        #######################################################################
        ## Interpret state information from GROUND station
        #######################################################################

        new_state = radio.read();
        
        # If we got a state command via telemetry, parse it and set latches
        if new_state != "":
            new_state = ord(new_state)  # convert from char to int
            debug("New state read (%d)." % new_state)

            # Get bit flags from new state
            arm       = state.get_bit(state.ARM_BIT, byte=new_state)
            logging   = state.get_bit(state.LOGGING_BIT, byte=new_state)
            chute     = state.get_bit(state.CHUTE_BIT, byte=new_state)
            power_off = state.get_bit(state.POWER_OFF_BIT, byte=new_state)

            ### Arm rocket ###
            if arm:
                if not _armed:
                    _armed = True
                    debug("Armed")
                    print "Armed"
            else:
                if _armed:
                    _armed = False
                    debug("Disarmed")
                    print "Disarmed"

            ### Data logging (sensor data and video) ###
            if logging:
                if not _logging_on:
                    # Initialize logger, which will create a new log file and
                    # set up the camera so we're ready to record. Start the
                    # camera too.
                    logger._init_new_log()
                    # logger.start_video()
                    t0 = time.time()  # reset reference time
                    _logging_on = True
                    debug("Started logging")
                    print "Started logging"
            else:
                if _logging_on:
                    # Stop data and camera and safely close file on disk.
                    logger.stop()  # stop only LOG, not DEBUG
                    _logging_on = False
                    debug("Stopped logging")
                    print "Stopped logging"

            ### Deploy chute ###
            if chute:
                if not _chute_deployed and _armed:
                    chute_pin.set_high()
                    _chute_deployed = True
                    time_chute_deployed = time.time()
                    debug("Chute pin HIGH")
                    print "Set chute pin to HIGH"

            ### Power off ###
            if power_off:
                if not _armed and not _logging_on:
                    print "Powering off"
                    time.sleep(1)  # give everything a chance to die
                    debug("Power off")
                    logger.stop(target=DEBUG)  # flush and close debug file
                    os.system("sudo poweroff")

        #######################################################################
        ## Do repeated actions (i.e. read from sensors) depending on latches
        #######################################################################
        
        # If logging is on, write IMU data to logfile! We have yet to implement
        # sensor logging from the BMP280 because its read speed is slower than
        # from the IMU.
        #
        # We are currently logging 14 data points, which will be transmitted as
        # 4-byte floats across the wireless network during UDP debugging. This
        # is 4*14 = 56 bytes (plus header) per UDP packet.
        if _logging_on:
            # Read from IMU
            data = sensor.read_imu()
            if data is not None:
                t = time.time() - t0
                debug("[%s] Data read" % t)
                data_vector = [t, state.state,
                    data["fusionPose"][0], data["fusionPose"][1], data["fusionPose"][2],
                    data["compass"][0],    data["compass"][1],    data["compass"][2],
                    data["accel"][0],      data["accel"][1],      data["accel"][2],
                    data["gyro"][0],       data["gyro"][1],       data["gyro"][2]]
                logger.write(data_vector)
                # If wifi debugging is enabled, send the data over UDP.
                if UDP_DEBUG:
                    wifidebugger.send(data_vector)
            #else:
            #    logger.write([time.time()-t0, "IMU_NOT_READY"])

        # Set chute pin back to LOW if blast cap burn time is reached
        if _chute_deployed and (time.time() - time_chute_deployed > BLAST_CAP_BURN_TIME):
            chute_pin.set_low()
            _chute_deployed = False
            debug("Chute pin LOW")
            print "Set chute pin to LOW"

        #######################################################################
        ## Update GROUND station
        #######################################################################

        # Update ground station once per HEARTBEAT_DELAY
        if time.time() - state_last_sent > HEARTBEAT_DELAY:
            state.set(state.IDLE)  # clear state and rebuild
            if _armed:          state.add(state.ARM)
            if _logging_on:     state.add(state.LOGGING)
            if _chute_deployed: state.add(state.CHUTE)
            radio.write(chr(state.state))
            state_last_sent = time.time()
            debug("Sent heartbeat (%d)" % state.state)
