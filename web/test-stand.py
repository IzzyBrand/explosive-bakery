from flask import Flask, render_template, request
import random

# system tools
import sys
import shutil
import os
import time

# IO tools
import subprocess
import json
import csv

# math tools
import numpy as np
#import scipy.integrate as spi

## SET UP VARIABLES
global testProcess

app = Flask(__name__)

ONLED     = 3
STATUSLED = 4
RELAYPIN  = 10

# log file name
# before changing this, rename all of current verison to new version
LOG_NAME = 'log.txt'

# True  : run on local computer,
# False : run on test stand
TESTING = True

# change into script directory, explosive-bakery/web
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

## GPIO SETUP

# setup GPIO if not in test mode

pins = {
    ONLED     : {'name': 'Power LED', 'state' : True},
    STATUSLED : {'name': 'Status LED', 'state' : False},
    RELAYPIN  : {'name': 'Relay Pin', 'state': False}
}

if not TESTING:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.bcm)

    # set pins
    for pin in pins:
       GPIO.setup(pin, GPIO.OUT)
       GPIO.output(pin, GPIO.LOW if pins[pin]['state'] else GPIO.HIGH)

def path_from_id(ident):
    def checker(x):
        if len(x) < 4:
            return False
        else:
            try:
                int(x[0:3])
                return True
            except ValueError:
                return False
    
    filt = lambda x: int(x[0:3]) == int(ident)
    id_folders = filter(filt, filter(checker, os.listdir('tests')))
    if len(id_folders) > 1:
        raise Exception('two folders found with matching id')
    elif len(id_folders) == 0:
        raise Exception('folder doesn\'t exist')
    else:
        return 'tests/%s' % id_folders[0]

## ROUTES
# index : get current pin state, return pin data on index
@app.route("/")
def main():
    global TESTING
    # For each pin, read the pin state and store it in the pins dictionary:
    if not TESTING:
        for pin in pins:
            pins[pin]['state'] = GPIO.input(pin)

    # Put the pin dictionary into the template data dictionary:
    templateData = {'pins' : pins, 'launchReady' : False}
    return render_template('bnasa.html', data=templateData)

# maketest : initializes a new test from a form with the required information,
#            batch name, launch date, rocket information
@app.route('/maketest', methods=['GET', 'POST'])
def maketest():
    info = dict(request.form)
    # count number of tests and increment for this one
    dirs = os.walk('tests').next()[1]
    ident = len(dirs) + 1
    if ident < 10:
        id_str = '00%s' % ident
    elif ident >= 10 and ident < 100:
        id_str = '0%s' % ident
    else:
        id_str = '%s' % ident

    folder_name = './tests/%s-%s' % (id_str, info['new-test-name'][0])
    os.mkdir(folder_name)
    returnData = {'worked': True,
                  'id': ident,
                  'folder': folder_name}

    return json.dumps(returnData)

# starttest
@app.route('/starttest/<ident>')
def starttest(ident):
    global testProcess
    testProcess = subprocess.Popen(['python', 'looper.py',
                                    path_from_id(ident)])
    return 'true'

@app.route('/readload')
def readload():
    return json.dumps(random.randint(0, 10000))

@app.route('/stoptest/<ident>')
def stoptest(ident):
    global testProcess
    testProcess.send_signal(2)
    time.sleep(0.01)
    return json.dumps(open('/tmp/hi.txt').read())

@app.route('/cancel/<ident>')
def canceltest(ident):
    # first three letters of test folder are their id
    # here, get the corresponding folder and delete it
    shutil.rmtree(path_from_id(ident))    
    return 'true'

@app.route('/getdata')
def getdata():
    # right now, just get all the folders no info about them
    def checker(x):
        if len(x) < 4:
            return False
        else:
            try:
                int(x[0:3])
                return True
            except ValueError:
                return False
    
    folders = filter(checker, os.listdir('tests'))
    ids = map(lambda x: int(x[0:3]), folders)
    return json.dumps(zip(folders, ids))

@app.route('/transferdata/<ident>')
def transfer_data(ident):
    path = os.path.join(path_from_id(ident), LOG_NAME)
    f = open(path, 'r')
    data = f.read()
    f.close()
    data = map(lambda x: map(float, x.split(', ')),
               filter(None, data.split('\n')))
    return json.dumps(data)

# The function below is executed when someone requests a URL with
# the pin number and action in it
def updatePin(changePin, action):
    # Convert the pin from the URL into an integer:
    changePin = int(changePin)
    # If the action part of the URL is "on," execute the code indented below:
    if action == "on":
        # Set the pin high:
        GPIO.output(changePin, GPIO.HIGH)
        # Save the status message to be passed into the template:
        message = "Turned {} on.".format(changePin)
    if action == "off":
        GPIO.output(changePin, GPIO.LOW)
        message = "Turned {} off.".format(changePin)

    if action == "toggle":
        # Read the pin and set it to whatever it isn't (that is, toggle it):
        GPIO.output(changePin, not GPIO.input(changePin))
        message = "Toggled {}.".format(changePin)

    # For each pin, read the pin state and store it in the pins dictionary:
    for pin in pins:
        pins[pin]['state'] = GPIO.input(pin)

# POST with [lower_endpoint, upper_endpoint] data with JSON format
@app.route('/setendpoints/<ident>', methods=['GET', 'POST'])
def setendpoints(ident):
    lower, upper = request.json
    log_file = os.path.join(path_from_id(ident), LOG_NAME)
    f = open(log_file)
    data = map(lambda l: map(float, l),
               list(csv.reader(f)))

    f.close()
    filt = lambda row: row[0] >= lower and row[0] <= upper
    data = filter(filt, data)
    X = np.array(data)
    integrand = spi.trapz(X[:, 1], X[:,0])
    return json.dumps(integrand)

@app.route('/check')
def check():
    return 'true'

if __name__ == "__main__":
    ip = '0.0.0.0'
    if (len(sys.argv) > 1): ip = sys.argv[1]
    app.run(host=ip, debug=True)
