# Reginald #

I guess this is Carlson 2.0?!

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
