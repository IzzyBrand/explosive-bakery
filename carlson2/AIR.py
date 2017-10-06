#!/usr/bin/python

# Version 2 of Carlson air controller and logging system.
#
# 4 October 2017, Benjamin Shanahan.  

import time
import serial

from state import State
from telemetry import Telemetry
from logger import Logger
from sensor import Sensor
from gpio import Pin

HEARTBEAT_DELAY = 1  # seconds, how often do we send state to ground station

if __name__ == "__main__":

    # Latches
    arm             = False
    logging         = False
    deploy_chute    = False
    power_off       = False
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
    ## Initialize our external devices
    ###########################################################################

    # Initialize telemetry radio for communication with ground station
    radio = Telemetry()

    # Initialize the IMU and barometer sensors so that we can read from them
    sensor = Sensor()

    # Initialize the GPIO pins so that we can use them
    chute_pin = Pin(4)

    # Define logger but don't instantiate it here
    logger = None

    # Main loop
    t0 = 0
    while (True):

        #######################################################################
        ## Interpret state information from ground station
        #######################################################################

        new_state = radio.read();
        
        # If we got a state command via telemetry, parse it and set latches
        if new_state != "":

            new_state = ord(new_state)  # convert from char to int

            # Set flags for incoming new state
            arm       = state.get_bit(state.ARM_BIT, new_state)
            logging   = state.get_bit(state.LOGGING_BIT, new_state)
            chute     = state.get_bit(state.CHUTE_BIT, new_state)
            power_off = state.get_bit(state.POWER_OFF_BIT, new_state)

            ### Arm rocket ###
            if arm:
                if not _armed:
                    _armed = True
                    print "armed"
            else:
                if _armed:
                    _armed = False
                    print "disarmed"

            ### Data logging (sensor data and video) ###
            if logging:
                if not _logging_on:
                    # Initialize logger, which will create a new log file and
                    # set up the camera so we're ready to record. Start the
                    # camera too.
                    logger = Logger()
                    logger.start_video()
                    t0 = time.time()  # reset reference time
                    _logging_on = True
                    print "started logger"
            else:
                if _logging_on:
                    # Stop data and camera and safely close logfile on disk.
                    logger.stop()
                    _logging_on = False
                    print "stopped logger"

            ### Deploy chute ###
            if chute:
                if not _chute_deployed and _armed:
                    chute_pin.set_high()
                    _chute_deployed = True
                    time_chute_deployed = time.time()
                    print "set chute pin to HIGH"

            ### Power off ###
            if power_off:
                if not _armed and not _logging_on and not _video_on:
                    print "powering off"
                    time.sleep(3)  # give everything a chance to die

        #######################################################################
        ## Do repeated actions depending on latches
        #######################################################################
        
        # If data is on, log it!
        if _data_on:
            # Read from IMU (no barometer yet)
            data = sensor.read_imu()
            logger.write([time.time()-t0, state.state,
                data["fusionPose"][0], data["fusionPose"][1], data["fusionPose"][2],
                data["compass"][0],    data["compass"][1],    data["compass"][2],
                data["accel"][0],      data["accel"][1],      data["accel"][2],
                data["gyro"][0],       data["gyro"][1],       data["gyro"][2]])

        # Set chute pin back to LOW if burn time is reached
        if _chute_deployed and (time.time() - time_chute_deployed > Sensor.BLAST_CAP_BURN_TIME):
            chute_pin.set_low()
            _chute_deployed = False
            print "set chute pin to HIGH"

        #######################################################################
        ## Update ground station
        #######################################################################

        # Update ground station once per HEARTBEAT_DELAY
        if time.time() - state_last_sent > HEARTBEAT_DELAY:
            state.set(state.IDLE)  # clear state and rebuild
            if _armed:          state.add(state.ARM)
            if _logging_on:     state.add(state.LOGGING)
            if _chute_deployed: state.add(state.CHUTE)
            radio.write(chr(state.state))
            state_last_sent = time.time()