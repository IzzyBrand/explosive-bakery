# Raspberry Pi 3 Access Point / Client Switcher #

An access point allows computers to connect to and SSH into the Raspberry Pi even without a WiFi connection. When the Pi is in Access Point (AP) mode, you can connect to its wireless network with your computer and then SSH into it.

Scripts from [Lewis Cowles](https://gist.github.com/Lewiscowles1986/fecd4de0b45b2029c390).

## Getting Started ##

First, we need to set up the Pi as a wireless access point. This process requires an internet connection and will take several minutes to complete. When done, please reboot the Pi.

	$ sudo chmod +x rPi3-ap-setup.sh
	$ sudo ./rPi3-ap-setup.sh yourPassword123 yourAPName
	$ reboot

Once this process has completed, the Pi will automatically reboot into AP mode unless otherwise directed.

### Switching WiFi Modes ###

To switch the Pi back into Client mode (so that it will look for and connect to a wireless network as a client):

	$ sudo ./restart_client

To switch the Pi back into Access Point mode (so that it broadcasts its own wireless network and allows local computers to connect and SSH in):

	$ sudo ./restart_access_point