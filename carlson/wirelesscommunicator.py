# WirelessCommunicator
#
# Send data across a wireless network via UDP.
#
# 2 November 2017, Benjamin Shanahan.

import socket

class WirelessCommunicator:

    def __init__(self, host_ip="127.0.0.1", host_port=5000, target_ip="127.0.0.1", target_port=5001):
        self._set_host(host_ip, host_port)
        self._set_target(target_ip, target_port)

        # Open a UDP socket and bind a port
        self._open_socket()
        self._bind_port()
        print "Opened socket and bound to %s, port %d." % (this_port, this_ip)
    
    ###########################################################################
    ## Manage Sockets and Ports
    ###########################################################################

    def _set_host(self, host_ip, host_port):
        self.host_ip = host_ip
        self.host_port = host_port

    def _set_target(self, target_ip, target_port):
        self.target_ip = target_ip
        self.target_port = target_port

    def _bind_port(self):
        self.sock.bind((self.host_ip, self.host_port))

    def _open_socket(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def _close_socket(self):
        self.sock.close()

    ###########################################################################
    ## Send and Receive Data
    ###########################################################################

    def send(self, message):
        self.sock.sendto(message, (self.target_ip, self.target_port))

    def receive(self, _buffer_size=1024):
        data, addr = self.sock.recvfrom(_buffer_size)
        return data, addr
