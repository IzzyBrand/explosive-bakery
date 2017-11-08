#!/usr/bin/python

# Wireless debugger process that sits on a laptop on the same wireless network
# as Carlson and listens to UDP packets containing data. It visualizes this
# data.
#
# The incoming data vector looks like this:
#   data_vector = [t, state.state,
#       data["fusionPose"][0], data["fusionPose"][1], data["fusionPose"][2],
#       data["compass"][0],    data["compass"][1],    data["compass"][2],
#       data["accel"][0],      data["accel"][1],      data["accel"][2],
#       data["gyro"][0],       data["gyro"][1],       data["gyro"][2]]
#
# 2 November 2017, Benjamin Shanahan.

import array
import wirelesscommunicator as wc

host_port   = 5001             # Port that Carlson will send to on this computer
target_ip   = "138.16.161.159"  # Carlson's IP address
target_port = 5000             # Carlson's port

def rad2deg(rad):
    return rad * 57.2958

def deg2rad(deg):
    return deg * 0.01745

if __name__ == "__main__":

    # Initialize WiFi debugger
    wifidebugger = wc.WirelessCommunicator(
        host_port=host_port, target_ip=target_ip, target_port=target_port,
        detect_netiface="wlp2s0")

    # Spin and listen for incoming data packets
    print "Waiting for data..."
    while(True):
        # Receive data from UDP socket (blocking)
        data_string, address = wifidebugger.receive()
        
        # Parse incoming byte string of floats, convert it to a list object.
        data_byte_array = array.array("f")
        data_byte_array.fromstring(data_string)
        data_vector = data_byte_array.tolist()

        #######################################################################
        ## Parse data so we can do something with it
        #######################################################################

        # Timestamp and current computer state
        t        = float(data_vector[0])
        state    = int(data_vector[1])

        # NOTE: Because of the way we calibrated the IMU, the cable needs to be
        #       pointed DOWNWARDS, and X and Y axes are switched.

        # Fusion pose
        fusionX  = rad2deg(float(data_vector[3]));
        fusionY  = rad2deg(float(data_vector[2]));
        fusionZ  = rad2deg(float(data_vector[4]));

        # Compass (magnetometer)
        compassX = float(data_vector[6]);
        compassY = float(data_vector[5]);
        compassZ = float(data_vector[7]);

        # Accelerometer
        accelX   = float(data_vector[9]);
        accelY   = float(data_vector[8]);
        accelZ   = float(data_vector[10]);

        # Gyroscope
        gyroX    = float(data_vector[12]);
        gyroY    = float(data_vector[11]);
        gyroZ    = float(data_vector[13]);

        #######################################################################
        ## Visualize Data
        #######################################################################

        print "%.4f (%d): %.4f %.4f %.4f" % (t, state, fusionX, fusionY, fusionZ)