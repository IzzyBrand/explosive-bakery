import os
import sys
import json
import numpy as np
import Adafruit_ADS1x15
import subprocess
import helpers
from datetime import datetime
import time
# Import the ADS1x15 module.

SCRIPT_PATH   = os.path.realpath(__file__)
SCRIPT_FOLDER = os.path.dirname(SCRIPT_PATH)
BAKERY_FOLDER = os.path.dirname(SCRIPT_FOLDER)
DATA_FOLDER   = os.path.join(BAKERY_FOLDER, 'thrust-tests')

logging = helpers.logging

class ThrustTest(object):
    def __init__(self, JSON=None, name=None, set_opts=False):
        if JSON is None and name is None:
            e = 'ThrustTest requires name or JSON argument'
            raise TypeError(e)
        elif JSON is None and name is not None:
            logging.debug('Initializing thrust test...')
            self.options = self.fresh_start(name, set_opts)
                
        elif JSON is not None and name is None:
            self.options = self.load_json(JSON, set_opts)
        else:
            e = 'ThrustTest cannot be called with both name and JSON arguments'
            raise TypeError(e)

        self.datestr = datetime.now().strftime('%d-%m-%y')

    def __str__(self):
        return '<Test "%s" on "%s">' % (self.name, self.datestr)

    def __repr__(self):
        return '<ThrustTest object on date "%s">' % self.datestr

    def fresh_start(self, name, set_opts):
        return helpers.init_test(name, set_opts)

    def load_json(self, path, set_opts):
        opts = json.load(open(path))
        if set_opts:
            return helpers.get_opt_dict(opts)
        else:
            return opts


    def run_test(self, test=False):
        # Create an ADS1115 ADC (16-bit) instance.
        self.adc = Adafruit_ADS1x15.ADS1015()
        self.GAIN = 1
        self.RATE = 3300 #128, 250, 490, 920, 1600, 2400, 3300
        
        times, thrusts = self.get_data(test=test)

        self.options['date'] = datetime.now().strftime('%d-%m-%y-%H-%M-%S')
        self.options['data']['ms'] = times
        self.options['data']['thrusts'] = thrusts
        self.options['complete'] = True
        # and organize the JSON
        json_path = os.path.join(os.path.dirname(BAKERY_FOLDER),
                                 self.options['datafile'])
        self.json_path = json_path
        json.dump(helpers.json_sort(self.options),
                  open(json_path, 'w'), indent=2)
        logging.debug('Data written to JSON file...')

    def get_data(self, test=False):
        if test:
            times = list(np.random.randn(100))
            thrusts = list(np.random.randn(100))
            return times, thrusts

        print '############         %s          ############' % self.options['name']
        times = []
        thrusts = []
        for x in range(50):
            try:
                adc.read_adc_difference(0, gain=self.GAIN, data_rate=self.RATE)
            except:
                logging.critical('Error in ADC read')
                raw_input('Enter to try again, ctrl-c to quit...')

        try:
            raw_input('Enter to begin logging, <ctrl-c> to quit...')
        except KeyboardInterrupt:
            logging.warning('Quitting... (paths not removed)')
            sys.exit(0)

        start_time = time.time()
        while True:
            try:
                time = time.time() - start_time
                thrust = adc.read_adc_difference(0, gain=self.GAIN, data_rate=self.RATE)
                times.append(time)
                thrusts.append(thrust)
            except KeyboardInterrupt:
                print ''
                logging.debug('Logging complete...')
                break
            except Exception as e:
                print 'Unknown error', e

        return times, thrusts

    def analyze(self):
        subprocess.call(['python', os.path.join(SCRIPT_FOLDER, 'analyze'),
                         '-j', self.json_path])

