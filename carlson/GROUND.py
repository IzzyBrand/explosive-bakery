# Carlson Ground Control v0.2
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

from state import State
from telemetry import Telemetry, PORT

import sys
import threading
import Queue
import argparse

state = State()

###############################################################################
## Functions
###############################################################################

# Asynchronously add any screen input to a queue
def add_input(input_queue):
    while True:
        input_queue.put(sys.stdin.read(1))

def broadcast(cmd=None):
    if cmd is not None:
        radio.write(chr(cmd))

###############################################################################
## Input Buffer
###############################################################################

# Set up argument parser to specify different port for radio via terminal
parser = argparse.ArgumentParser(description="Ground station for the Carlson rocket flight computer.")
parser.add_argument('-p', '--port', default=PORT, help='Serial port of the telemetry radio.')
args = parser.parse_args()

# Initialize Telemetry radio
radio = Telemetry(args.port)

# Add Queue and launch a thread to monitor user input.
input_queue = Queue.Queue()
input_thread = threading.Thread(target=add_input, args=(input_queue,))
input_thread.daemon = True
input_thread.start()

# Respond to user input, non-blocking.
while (True):

    if not input_queue.empty():
        arg = input_queue.get().lower().strip()
        if arg != "":   # and arg in commands:
            # Arm
            if arg == "a":
                print "arm"
                broadcast(state.ARM)
            # Disarm
            if arg == "d":
                print "disarm"
                broadcast(state.IDLE)
            # Start logger (i.e. ready for launch)
            if arg == "l":
                print "start logging"
                broadcast(state.ARM + state.LOGGING)
            # Deploy chute
            if arg == "c":
                print "deploy chute"
                broadcast(state.ARM + state.LOGGING + state.CHUTE)
            # Shutdown Carlson
            if arg == "k":
                print "power off"
                broadcast(state.POWER_OFF)

    # Read (non-blocking) from telemetry radio
    received = radio.read()
    if received != "":
        state.set(ord(received))
        print "Air State: %s" % state