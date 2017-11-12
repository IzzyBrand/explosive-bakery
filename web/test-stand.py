from flask import Flask, render_template, request
import subprocess
import sys
test = True
if not test:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.bcm)

app = Flask(__name__)

# stores the background tast
background_task = None

# Create a dictionary called pins to store the pin number, name, and pin state:
pins = {
    24 : {'name': 'LED', 'state' : True},
}

# Set each pin as an output and make it low:
if not test:
    for pin in pins:
       GPIO.setup(pin, GPIO.OUT)
       GPIO.output(pin, GPIO.LOW)

@app.route("/")
def main():
    global test
    # For each pin, read the pin state and store it in the pins dictionary:
    if not test:
        for pin in pins:
            pins[pin]['state'] = GPIO.input(pin)

    # Put the pin dictionary into the template data dictionary:
    templateData = {'pins' : pins, 'launchReady' : False}
    return render_template('bnasa.html', data=templateData)


# The function below is executed when someone requests a URL with the pin number and action in it:
@app.route("/set/<changePin>/<action>")
def action(changePin, action):
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

   # Along with the pin dictionary, put the message into the template data dictionary:
    templateData = {
        'message' : message,
        'pins' : pins
    }

    return render_template('bnasa.html', **templateData)

@app.route('/bogusstart')
def bogustrue():
    templateData = {'pins': pins, 'launchReady': True}
    return render_template('bnasa.html', data=templateData)

@app.route("/bgstart")
def start_background_task():
    global background_task
    background_task = subprocess.Popen(['python', 'background_task.py'],
                                       stdin=subprocess.PIPE,
                                       stdout=subprocess.PIPE)
    print background_task
    return 'Background task started at ' + str(background_task)

@app.route("/bgstop/<msg>")
def stop_background_task(msg):
    global background_task
    background_task.stdin.write("{}\n".format(msg))
    background_task_return = background_task.stdout.read()
    return 'Background tast stopped. It returned {}'.format(background_task_return)

if __name__ == "__main__":
    ip = '127.0.0.1'
    if (len(sys.argv) > 1): ip = sys.argv[1]
    app.run(host=ip, debug=True)
