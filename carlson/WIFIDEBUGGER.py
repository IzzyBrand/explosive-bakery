# Wireless debugger process that sits on a laptop on the same wireless network
# as Carlson and listens to UDP packets containing data. It visualizes this
# data.
#
# 2 November 2017, Benjamin Shanahan.

import wirelesscommunicator as wc

host_port   = 5001             # Port that Carlson will send to on this computer
target_ip   = "192.168.1.226"  # Carlson's IP address
target_port = 5000             # Carlson's port

if __name__ == "__main__":

    # Initialize WiFi debugger
    wifidebugger = wc.WirelessCommunicator(
        host_port=host_port, target_ip=target_ip, target_port=target_port)

    # Spin and listen for incoming data packets
    print "Waiting for data..."
    while(True):
        data_string, address = wifidebugger.receive()
        data_vector = data_string.split(",")
        
        print data_vector[0], data_vector[1], data_vector[2], data_vector[3]