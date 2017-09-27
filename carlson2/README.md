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

## Additional Notes ##

We may want to eventually integrate the Barometer code into RTIMULib2 so that we can perform all sensor readings at a closer timestep. For now it's probably fine to keep them as separate Python libraries.
