# Carlson Ground Control v0.1
#
# Sending commands to the rocket:
#    The rocket, after receiving and doing a command, will respond to the 
#    ground station with the same command code that it received. For
#    example, if we want to arm the rocket, we send "a". The rocket receives
#    this, proceeds to arm sequence, and then sends back "a" to confirm that it
#    has done the requested command. Ground continues to send "a" with a short 
#    time delay until it has received a confirmation response.
#
# See here for model code: https://stackoverflow.com/questions/2408560/python-nonblocking-console-input
#
# Benjamin Shanahan

import config  # configuration file

import serial
import struct
import sys
import threading
import Queue

from time import time, sleep

telem = serial.Serial(port=config.port, baudrate=config.baud, timeout=config.serial_timeout)
print "Initialized telemetry on port %s at baud %d." % (config.port, config.baud)

commands      = dict
time_cmd_send = 0
got_response  = True
current_cmd   = None
is_armed      = False

###############################################################################
## Functions
###############################################################################

# Thread function
def add_input(input_queue):
    while True:
        input_queue.put(sys.stdin.read(1))

def send_telem(cmd=None):
    global got_response, current_cmd, time_cmd_send
    if (cmd is not None and got_response) or (not got_response and cmd == current_cmd):
        telem.write(cmd)
        time_cmd_send = time()
        current_cmd   = cmd
        got_response  = False

def quit():
    exit()

def print_help():
    for name, info in commands.iteritems():
        print "%s: %s" % (name, info["help"])

###############################################################################
## Commands
###############################################################################

commands = {
    config.ARM: {
        "say": "Arming rocket.",
        "success": "Rocket is armed.",
        "function": send_telem,
        "parameter": "a",
        "help": "Arm the rocket."
    },
    config.CHECK: {
        "say": "Initiating self-check of sensor readings.",
        "success": "Sensor values OK.",
        "function": send_telem,
        "parameter": "c",
        "help": "Tell rocket to verify that its sensor readings make sense."
    },
    config.DEPLOY: {
        "say": "Deploying parachute.",
        "success": "Rocket deployed chute.",
        "function": send_telem,
        "parameter": "d",
        "help": "Deploy the parachute."
    },
    config.STOP: {
        "say": "Stopping data logging.",
        "success": "Rocket stopped data logging.",
        "function": send_telem,
        "parameter": "x",
        "help": "Stop logging data to SD card."
    },
    config.HELP: {
        "say": "Recognized commands:",
        "function": print_help,
        "parameter": None,
        "help": "Get help."
    },
    config.QUIT: {
        "say": "Goodbye.",
        "function": quit,
        "parameter": None,
        "help": "Quit."
    }
}

###############################################################################
## Input Buffer
###############################################################################

print "Ground station boot successful. Type '%s' for help." % config.HELP
raw_input("Press ENTER once rocket is powered on.")
print ""

# Add Queue and launch a thread to monitor user input.
input_queue = Queue.Queue()
input_thread = threading.Thread(target=add_input, args=(input_queue,))
input_thread.daemon = True
input_thread.start()

# Respond to user input, non-blocking.
last_heartbeat = time()
while (True):

    # Update heartbeat timer (if rocket is unarmed)
    if not is_armed:
        if time() - last_heartbeat > config.heartbeat_max_delay:
            print "No heartbeat received in last %d seconds!" % config.heartbeat_max_delay
            sleep(config.time_before_resend)

    if not input_queue.empty():
        arg = input_queue.get().lower().strip()
        if arg != "":
            if arg == config.HELP or arg == config.QUIT or (is_armed and arg in commands):
                cmd_info = commands[arg]
                print cmd_info["say"]
                if cmd_info["parameter"] is None:
                    cmd_info["function"]()
                else:    
                    cmd_info["function"](cmd_info["parameter"])
            elif not is_armed:
                if arg == config.ARM:  # allow rocket to be armed
                    send_telem(arg)
                else:
                    print "Rocket must be armed before sending commands."
            elif arg == "":
                pass
            else:
                print "Command '%s' not recognized. Type '%s' for help." % (arg, config.HELP)

    # Read (non-blocking) from telemetry radio
    response = telem.read(1)
    if response != "":
        if response != config.HEARTBEAT:
            if response == config.ARM:
                is_armed = True
            # Print to console the command that we just received
            print "\n=== Carlson transmission ==="
            print commands[response]["success"]
            print "===== End transmission ====="
            # Did we receive a response to the command we sent?
            if response in commands and response == current_cmd:
                got_response = True
        elif response == config.HEARTBEAT:
            last_heartbeat = time()
        else:
            print "Unrecognized packet (%s)!" % response

    if not got_response and (time() - time_cmd_send > config.time_before_resend):
        print "No response, resending '%s' command." % current_cmd
        send_telem(current_cmd)