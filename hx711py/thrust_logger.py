import RPi.GPIO as GPIO
import numpy as np
import time
import sys
import os
from hx711 import HX711
from datetime import datetime

DATA_PIN    = 5
CLOCK_PIN   = 6
LED_PIN     = 23
RELAY_PIN   = 24

class ThrustLogger():
    def __init__(self, filename):
        bakery = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.data_directory = '%s/web/thrust-tests' % bakery
        self.prep_file(filename)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(LED_PIN, GPIO.OUT)
        GPIO.setup(RELAY_PIN, GPIO.OUT)
        GPIO.output(LED_PIN, False)
        GPIO.output(RELAY_PIN, False)
        self.ignite_start = -1
        self.ignite_duration = 2.
        self.hx = HX711(DATA_PIN, CLOCK_PIN)
        self.hx.set_reading_format("LSB", "MSB")
        self.hx.set_reference_unit(92)
        self.hx.reset()
        self.hx.tare(100)
        self.start_time = time.time()
        self.times = []
        self.triggered = False
        self.thrusts = []
        GPIO.output(LED_PIN, True)

    def step(self):
        self.times.append(time.time() - self.start_time)
        self.thrusts.append(self.hx.get_one() * -1.)
        if self.ignite_start == -1 and self.times[-1] > 0.2:
            if self.verify_data():
                print 'IGNITER ON'
                self.ignite_start = self.times[-1]
                GPIO.output(RELAY_PIN, True)
            else: print 'Data is too homogenous or not enough readings. Waiting to ignite.'
        elif self.times[-1] - self.ignite_start > self.ignite_duration and not self.triggered:
            print 'IGNITER OFF'
            self.triggered = True
            GPIO.output(RELAY_PIN, False)

    def verify_data(self):
        return len(self.thrusts) > 10 and (min(self.thrusts) != max(self.thrusts))

    def prep_file(self, filename):
        self.foldername = self.data_directory + '/' + filename.replace(" ","")
        self.filename = self.foldername + '/' + (filename if filename.endswith(".txt") else (filename + ".txt"))
        if os.path.exists(self.filename):
            print self.filename, 'already exists. Please choose another name.'
            sys.exit(1)
        elif os.path.isdir(self.foldername):
            print 'Found', self.foldername, ' and logging there.'
        else:
            os.makedirs(self.foldername)

    def write_log(self):
        try:
            with open(self.filename, 'w') as f:
                for time, thrust in zip(self.times, self.thrusts):
                    f.write('{},{}\n'.format(time, thrust))
            print 'Data written to', self.filename
        except Exception as e:
            backup_filename = datetime.now().strftime("backup_%Y-%m-%d_%H:%M:%S.txt")
            print 'Failed to write to {}. Saving backup to {}.'.format(self.filename, backup_filename)
            with open(backup_filename, 'w') as f:
                for time, thrust in zip(self.times, self.thrusts):
                    f.write('{},\t{}\n'.format(time, thrust))
            print 'Data written to', backup_filename

    def cleanup(self):
        GPIO.output(LED_PIN, False)
        GPIO.output(RELAY_PIN, False)
        GPIO.cleanup()


if __name__ == '__main__':
    if len(sys.argv) > 1: 
        filename = sys.argv[1]
    else:
        print 'You have to provide a filename for the test!'
        sys.exit(1)

    logger = ThrustLogger(filename)
    while True:
        try:
            logger.step()
        except KeyboardInterrupt:
            print 'interrupt'
            break
        except Exception as e:
            print e
            break

    logger.write_log()
    logger.cleanup()
    sys.exit(0)
