# Carlson v0.3 #

Carlson is a Raspberry Pi Zero based rocket flight computer with an MPU9255 IMU, BMP280 barometer, 1080p video camera, WiFi chip, and 915 MHz telemetry radio. It runs on a two-cell lithium polymer battery. Carlson will eventually control automatic apogee detection in flight and parachute deployment.

## Installation ##

**GROUND**

    $ pip install -r requirements/ground.txt

**AIR**

Follow directions under *Additional Repositories* below to compile and install sensor libraries. Then,

    $ pip install -r requirements/air.txt

## AIR station ##

Python state machine running on the Raspberry Pi in the rocket that starts and stops data / video logging and can detonate the parachute ejection blast cap in flight. This script sends periodic updates to the GROUND station via telemetry at 1 Hz and listens for incoming state transition commands from GROUND. 

## GROUND station ##

Python ground server script. This is a lite version of what will eventually run on the base station, controlled by the web server (users will interact with the system through a front-end web-page server by the web server). The ground script serves up an input terminal where user can manually input commands. Data received from the AIR station is printed in the terminal as soon as it arrives.

#### Available Commands

Coming soon. For now, just check out the GROUND.py source code.

## Additional Repositories ##

These repositories have been forked so that we can modify them as required. They both require compilation and installation before they can be used.

### Accel/Gyro/Magnet ###

https://github.com/benshanahan1/RTIMULib2

For compilation on Linux systems, see https://github.com/benshanahan1/RTIMULib2/tree/master/Linux.

### Barometer ###

https://github.com/benshanahan1/BMP280

This is just a C++ python library that needs to be compiled. Run:

	$ sudo python setup.py build
	$ sudo python setup.py install

## Telemetry Link ##

We are using a pair of 915 MHz 3DR telemetry radios to communicate between AIR and GROUND. This radio link enables two-way communication between the AIR and GROUND stations.

## To Do ##

1. Calibrate IMU before next flight (check orientation flags for mounting in rocket)
2. Update requirements/air.txt
3. Incorporate barometer data