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
    def __init__(self):
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
        self.thrusts = []
        GPIO.output(LED_PIN, True)

    def step(self):
        self.thrusts.append(self.hx.get_one() * -1.)
        sys.stdout.write('%s\n' % self.thrusts[-1])

    def verify_data(self):
        return len(self.thrusts) > 10 and (min(self.thrusts) != max(self.thrusts))

    def cleanup(self):
        GPIO.output(LED_PIN, False)
        GPIO.output(RELAY_PIN, False)
        GPIO.cleanup()


if __name__ == '__main__':
    logger = ThrustLogger()
    while True:
        try:
            logger.step()
        except KeyboardInterrupt:
            print 'interrupt'
            break
        except Exception as e:
            print e
            break

    logger.cleanup()
    sys.exit(0)
