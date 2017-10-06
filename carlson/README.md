# Carlson v0.3 #

Carlson is a Raspberry Pi Zero based rocket flight computer with an MPU9255 IMU, BMP280 barometer, 1080p video camera, WiFi chip, and 915 MHz telemetry radio. It runs on a two-cell lithium polymer battery. Carlson will eventually control automatic apogee detection in flight and parachute deployment.

## AIR station ##

Python state machine running on the Raspberry Pi in the rocket that starts and stops data / video logging and can detonate the parachute ejection blast cap in flight. This script sends periodic updates to the GROUND station via telemetry at 1 Hz and listens for incoming state transition commands from GROUND. 

## GROUND station ##

Python ground server script. This is a lite version of what will eventually run on the base station, controlled by the web server (users will interact with the system through a front-end web-page server by the web server). The ground script serves up an input terminal where user can manually input commands. Data received from the AIR station is printed in the terminal as soon as it arrives.

#### Available Commands

Coming soon. For now, just check out the GROUND.py source code.

## Additional Repositories ##

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

## To Do ##

1. Calibrate IMU before next flight (check orientation flags for mounting in rocket)
2. Add requirements.txt (one for AIR station requirements, and one for GROUND station requirements).
3. Incorporate barometer data