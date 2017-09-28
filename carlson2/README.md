# Carlson v2.0 #

## air.py ##

Python script running on the Raspberry Pi in the rocket. This script does the following:

1. Start on Pi boot.
2. Send heartbeats at a regular interval across telemetry radio to ground station until "arm" command is received.
3. When "arm" command received, stop heartbeats, send "armed" confirmation to ground station, and begin saving sensor data to file. Send "started logging" confirmation to ground.
4. Rocket can be launched.
5. During flight, sensor data is logged, and telemetry radio is being checked (non-blocking) for commands from ground.
6. If command "deploy chute" is received, GPIO pin is triggered and parachute deployed.
7. If command "stop logging" is received, save and flush log file and stop logging. Send "stopped logging" confirmation to ground.

Do we want to add live calibration (in the field)?

## ground.py ##

Python ground server script. This is a lite version of what will eventually run on the base station, controlled by the web server (users will interact with the system through a front-end web-page server by the web server).

The ground script serves up an input terminal where user can manually input commands. Data received from air script is printed in the terminal when it arrives.

#### Available Commands ####

- arm [ `a` ]
    - effect: stops heartbeats from rocket, starts data logging, rocket is flight ready
    - response: "armed"
- deploy (chute) [ `d` ]
    - effect: deploys rocket parachute
    - response: "chute deployed"
- stop (data logging) [ `x` ]
    - effect: stop data logging
    - response: "stopped logging"

Additional commands (these may or may not be implemented):

- calibrate
- reboot
- shutdown
- disarm

## Repositories ##

These repositories have been forked so that we can modify them as required. They both require compilation before they can be used.

### Accel/Gyro/Magnet ###

https://github.com/benshanahan1/RTIMULib2

For compilation on Linux systems, see https://github.com/benshanahan1/RTIMULib2/tree/master/Linux.

### Barometer ###

https://github.com/benshanahan1/BMP280

This is just a C++ python library that needs to be compiled. Run:

	$ sudo python setup.py build
	$ sudo python setup.py install

## Telemetry Link ##

We are using a pair of 915 MHz 3DR telemetry radios to communicate between the rocket with Carlson and our wireless base-station or laptop running the Python logging manager. This radio link allows data to be transmitted back to the ground from Carlson in-flight, giving us close-to-realtime estimates of attitude, orientation in space, and eventually velocity. This communication tunnel is two way, allowing us to manually deploy the parachute by sending a command back to Carlson inside of the rocket.

## Additional Notes ##

We may want to eventually integrate the Barometer code into RTIMULib2 so that we can perform all sensor readings at a closer timestep. For now it's probably fine to keep them as separate Python libraries.
