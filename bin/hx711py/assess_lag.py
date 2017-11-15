import RPi.GPIO as GPIO
import time
import sys
from hx711 import HX711


DATA_PIN = 5
CLOCK_PIN = 6

hx = HX711(DATA_PIN, CLOCK_PIN)

hx.set_reading_format("LSB", "MSB")

hx.set_reference_unit(92)

start_t = time.time()
prev_t = time.time()
max_lag = 0
counter = 0
while True:
    try:
        t = time.time()
        dt = t - prev_t
        hx.get_one()
        if dt > max_lag:
            print '{}th maximum lag {} at time {}.'.format(counter,max_lag, time.time() - start_t)
            max_lag = dt
            counter += 1
        prev_t = t

    except (KeyboardInterrupt, SystemExit):
        print "\nCleaning..."
        GPIO.cleanup()
        print "Bye!"
        sys.exit()
