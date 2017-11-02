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

import wirelesscommunicator as wc

host_port   = 5001             # Port that Carlson will send to on this computer
target_ip   = "192.168.1.226"  # Carlson's IP address
target_port = 5000             # Carlson's port

def rad2deg(rad):
    return rad * 57.2958

def deg2rad(deg):
    return deg * 0.01745

if __name__ == "__main__":

    # Initialize WiFi debugger
    wifidebugger = wc.WirelessCommunicator(
        host_port=host_port, target_ip=target_ip, target_port=target_port)

    # Spin and listen for incoming data packets
    print "Waiting for data..."
    while(True):
        data_string, address = wifidebugger.receive()
        data_vector = data_string.split(",")

        #######################################################################
        ## Parse data so we can do something with it
        #######################################################################
        
        # Timestamp and current computer state
        t        = float(data_vector[0])
        state    = int(data_vector[1])

        # NOTE: the X Y Z and not in that order because we offset the IMU axes,
        #       so we need to figure out the order if it changesand adjust it
        #       below.

        # Fusion pose
        fusionX  = rad2deg(float(data_vector[2]));
        fusionY  = rad2deg(float(data_vector[4]));
        fusionZ  = rad2deg(float(data_vector[3]));

        # Compass (magnetometer)
        compassX = float(data_vector[5]);
        compassY = float(data_vector[7]);
        compassZ = float(data_vector[6]);

        # Accelerometer
        accelX   = float(data_vector[8]);
        accelY   = float(data_vector[10]);
        accelZ   = float(data_vector[9]);

        # Gyroscope
        gyroX    = float(data_vector[11]);
        gyroY    = float(data_vector[13]);
        gyroZ    = float(data_vector[12]);

        #######################################################################
        ## Visualize Data
        #######################################################################

        print "%.4f (%d): %.4f %.4f %.4f" % (t, state, fusionX, fusionY, fusionZ)