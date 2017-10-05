#!/usr/bin/python

# Version 2 of Carlson air controller and logging system.
#
# 4 October 2017, Benjamin Shanahan.  

import time
import serial

from config import State, Telemetry, Sensor, Logging


if __name__ == "__main__":

    # Latches
    arm             = False
    record_video    = False
    record_data     = False
    deploy_chute    = False
    power_off       = False
    _armed          = False
    _data_on        = False
    _video_on       = False
    _chute_deployed = False

    # Set current state of air controller and declare the time we last sent a 
    # state update to the ground station
    s               = State()
    state_last_sent = 0

    # Timing variables
    time_chute_deployed = 0

    # Keep looping until the telemetry radio connects
    while True:
        try:
            telemetry = serial.Serial(port=Telemetry.PORT,
                                  baudrate=Telemetry.BAUD,
                                  timeout=Telemetry.SERIAL_TIMEOUT)
            print "initialized telemetry radio"
            break
        except serial.serialutil.SerialException:
            print "telemetry not found, trying again"
            time.sleep(0.5)

    # Main loop
    while (True):

        #######################################################################
        ## Interpret state information from ground station
        #######################################################################

        new_state = telemetry.read(1);
        
        # If we got a state command via telemetry, parse it and set latches
        if new_state != "":

            new_state = ord(new_state)  # convert from char to int

            # Set flags for incoming new state
            arm       = s.get_bit(byte=new_state, s.ARM_BIT)
            video     = s.get_bit(byte=new_state, s.VIDEO_BIT)
            data      = s.get_bit(byte=new_state, s.DATA_BIT)
            chute     = s.get_bit(byte=new_state, s.CHUTE_BIT)
            power_off = s.get_bit(byte=new_state, s.POWER_OFF_BIT)

            ### Arm rocket ###
            if arm:
                if not _armed:
                    _armed = True
                    print "armed"
            else:
                if _armed:
                    _armed = False
                    print "disarmed"

            ### Data logging ###
            if data:
                if not _data_on:
                    _data_on = True
                    print "started data"
            else:
                if _data_on:
                    _data_on = False
                    print "stopped data"

            ### Video capture ###
            if video:
                if not _video_on:
                    # camera.start_recording()
                    _video_on = True
                    print "started video"
            else:
                if _video_on:
                    # camera.stop_recording()
                    _video_on = False
                    print "stopped video"

            ### Deploy chute ###
            if chute:
                if not _chute_deployed and _armed:
                    _chute_deployed = True
                    time_chute_deployed = time.time()
                    print "deployed chute"

            ### Power off ###
            if power_off:
                if not _armed and not _data_on and not _video_on:
                    print "powering off"
                    time.sleep(3)  # give everything a chance to die

        #######################################################################
        ## Do repeated actions depending on latches
        #######################################################################
        
        # if _data_on and imu.IMURead():
        #     # log sensor data to file
        #     pass

        if _chute_deployed and (time.time() - time_chute_deployed > Sensor.BLAST_CAP_BURN_TIME):
            _chute_deployed = False
            # ...
            print "set chute pin to low"

        #######################################################################
        ## Update ground station
        #######################################################################

        # Update ground station once per HEARTBEAT_DELAY
        if time.time() - state_last_sent > Telemetry.HEARTBEAT_DELAY:
            s.set(s.IDLE)  # clear state and rebuild
            if _armed:          s.add(s.ARM)
            if _data_on:        s.add(s.DATA)
            if _video_on:       s.add(s.VIDEO)
            if _chute_deployed: s.add(s.CHUTE)
            telemetry.write(chr(s.state))
            state_last_sent = time.time()