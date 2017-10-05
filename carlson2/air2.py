#!/usr/bin/python

# Version 2 of Carlson air controller and logging system.
#
# 4 October 2017, Benjamin Shanahan.  

import time
import serial

from config import State, Telemetry, Sensor, Logging


if __name__ == "__main__":

    # Latches
    armed           = False
    record_video    = False
    record_data     = False
    deploy_chute    = False
    power_off       = False
    _data_on        = False
    _video_on       = False
    _chute_deployed = False

    # Set current state of air controller and declare the time we last sent a 
    # state update to the ground station
    state           = State.IDLE
    _last_send_time = 0

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
        if new_state is not None and new_state.isdigit():

            state = int(new_state)

            # Set flags for incoming state
            armed        = State.get_bit(state, State.ARM_BIT)
            record_video = State.get_bit(state, State.RECORD_VIDEO_BIT)
            record_data  = State.get_bit(state, State.RECORD_DATA_BIT)
            deploy_chute = State.get_bit(state, State.DEPLOY_CHUTE_BIT)
            power_off    = State.get_bit(state, State.POWER_OFF_BIT)

            # Actions requiring rocket to be armed
            if armed:
                
                ### Data logging ###
                if record_data:
                    if not _data_on:
                        _data_on = True
                        print "started data"

                ### Video capture ###
                if record_video:
                    if not _video_on:
                        # camera.start_recording()
                        _video_on = True
                        print "started video"

                ### Deploy chute ###
                # Also requires that rocket has started recording data and video
                if deploy_chute:
                    if not _chute_deployed and _data_on and _video_on:
                        _chute_deployed = True
                        print "deployed chute"

            # These conditions can only be satisfied if rocket is disarmed
            else:

                ### Stop data logging ###
                if not record_data:
                    if _data_on:
                        _data_on = False
                        print "stopped data"

                ### Stop video capture ###
                if not record_video:
                    if _video_on:
                        # camera.stop_recording()
                        _video_on = False
                        print "stopped video"

                ### Power off ###
                if power_off:
                    if not _data_on and not _video_on:
                        print "powering off"
                        time.sleep(3)  # give everything a chance to die

        #######################################################################
        ## Do repeated actions depending on latches
        #######################################################################
        
        # if _data_on and imu.IMURead():
        #     # log sensor data to file
        #     pass

        #######################################################################
        ## Update ground station
        #######################################################################

        # Update ground station once per HEARTBEAT_DELAY
        if time.time() - _last_send_time > Telemetry.HEARTBEAT_DELAY:
            telemetry.write(str(state))
            _last_send_time = time.time()