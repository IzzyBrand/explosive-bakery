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
        self.data_directory = './thrust-tests/'
        self.prep_file(filename)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(LED_PIN, GPIO.OUT)
        GPIO.setup(RELAY_PIN, GPIO.OUT)
        self.ignite_start = -1
        self.ignite_duration = 5.
        self.hx = HX711(DATA_PIN, CLOCK_PIN)
        self.hx.reset()
        self.hx.tare()
        self.start_time = time.time()
        self.times = []
        self.thrusts = []
        GPIO.output(LED_PIN, True)

    def step(self):
        self.times.append(time.time() - start_time)
        self.thrusts.append(hx.get_one())
        if self.times[-1] > 1.0 and self.ignite_start == -1:
            print 'IGNITER ON'
            self.ignite_start = self.times[-1]
            self.GPIO.output(RElAY_PIN, True)
        elif self.times[-1] - self.ignite_start > self.ignite_duration:
            print 'IGNITER OFF'
            self.GPIO.output(RElAY_PIN, False)

    def prep_file(self, filename):
        self.foldername = self.data_directory + '/' + filename.replace(" ","")
        self.filename = self.foldername if self.foldername.endswith(".txt") else (self.foldername + ".txt")
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
                    f.write('{},\t{}\n').format(time, thrust)
            print 'Data written to', self.filename
        except Exception as e:
            backup_filename = datetime.now().strftime("backup_%Y-%m-%d_%H:%M:%S.txt")
            print 'Failed to write to {}. Saving backup to {}.'.format(self.filename, backup_filename)
            with open(backup_filename, 'w') as f:
                for time, thrust in zip(self.times, self.thrusts):
                    f.write('{},\t{}\n').format(time, thrust)
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
            break
        except Exception as e:
            print e
            break

    logger.write_log()
    logger.cleanup()
    sys.exit(0)