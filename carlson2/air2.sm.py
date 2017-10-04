# Version 2 of Carlson air controller and logging system.
#
# 4 October 2017, Benjamin Shanahan.

# Available states. We are passing one byte across telemetry, so the max number
# of possible states is 255.
IDLE          = 0     # default state on boot (sending heartbeats)
ARM           = 1     # arm / disarm rocket and allow other functionality
CAPTURE_VIDEO = 2     # start / stop camera capture
DEPLOY_CHUTE  = 4     # toggle parachute GPIO pin
RECORD_DATA   = 8     # start / stop recording sensor data to disk 
POWER_OFF     = 16    # shut down computer (last possible state)

# Retrieve value of bit at index in given byte. Return True if bit is 1.
def get_bit(byte_val, idx):
    return ((byte_val & (1 << idx)) != 0);

if __name__ == "__main__":
    # Set current state of air controller
    state = IDLE

    while (True):
        # TODO: make this input non-blocking
        # Air controller receives byte from ground requesting state transition
        new_state = raw_input(">> ");

        if new_state == "":
            continue
        else:
            state = int(new_state)

        # Parse state transition request
        if get_bit(state, 0):
            print "ARMED"
        else:
            print "DISARMED"
            
        # Video capture
        if get_bit(state, 1):
            print "Video ON"
        else:
            print "Video OFF"

        # Deploy chute
        if get_bit(state, 2):
            print "Chute pin HIGH"
        else:
            print "Chute pin LOW"

        # Record sensor data
        if get_bit(state, 3):
            print "Data recording ON"
        else:
            print "Data recording OFF"

        # Power down flight computer
        if get_bit(state, 4):
            print "Shutting down"