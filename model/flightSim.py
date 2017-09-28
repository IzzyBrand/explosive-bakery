import numpy as np
import argparse
import json
import os
import sys
import matplotlib.pyplot as plt
from parameters import *

if __name__ == '__main__':
    # set up the argparser
    ap = argparse.ArgumentParser()
    ap.add_argument("-j", "--json-file", default=None, type=str, required=True,
    help='JSON file to analyze')
    # ap.add_argument("-t", "--time-step", default=0.0001, type=float, required=True,
    # help='time step for simulatoion')
    args = vars(ap.parse_args())

    file_name = args['json_file']
    # time_step = args['time_step']

    # load the specified thrust data file
    thrusts = None
    times = None
    try:
        f = open(file_name)
        json_data = json.load(f)
        times = np.array(json_data['data']['ms'])
        thrusts = np.array(json_data['data']['thrusts'])
    except Exception as e:
        print e

    if times is not None and len(times) > 0:
        print 'Successfully loaded {} data points from {}'.format(len(times), file_name)
    else:
        print 'Failed to load data from', file_name
        sys.exit(1)



    # load the endpoints and cut the thrust data appropriately
    right_endpoint = None
    left_endpoint = None

    # try:
    #     right_endpoint = float(json_data['right_endpoint'])
    #     left_endpoint = float(json_data['left_endpoint'])
    # except Exception as e:
    #     print e

    # if right_endpoint is not None and left_endpoint is not None and right_endpoint > left_endpoint:
    #     print 'Using enpoints at {} and {} seconds'.format(left_endpoint,right_endpoint)


    # simulate
    pos = 0
    vel = 0
    accel = 0
    flight_data = np.zeros((len(times), 3))

    for i in range(len(times)-1):
        # if left_endpoint is None and times[i] > left_endpoint:
        #     if right_endpoint is not None and times[i] < right_endpoint:
        dt = times[i+1] - times[i]
        drag_force = - np.sign(vel) * drag_coefficient * vel**2 * air_density * surface_area
        thrust_force = thrusts[i] / 1000.0 * gravity

        accel = (thrust_force + drag_force) / total_mass - gravity 
        vel += accel * dt
        pos += vel * dt
        # correct position and velocity when on ground
        pos = max(pos, 0)
        if pos == 0: vel = max(0,vel)

        flight_data[i][0] = pos
        flight_data[i][1] = vel
        flight_data[i][2] = accel


        # time_step_interpolation_offset = 0
        # while times[i] + time_step_interpolation_offset < times[i+1]:
        #     curr_thrust = thrusts[i] * time_step_interpolation_offset/dt + thrusts[i+1] * 

        #     time_step_interpolation_offset += time_step
        
    maxes = np.max(flight_data, 0)
    print 'MAX ALTITUDE:\t\t{} m'.format(maxes[0])
    print 'MAX VELOCITY:\t\t{} m/s'.format(maxes[1])
    print 'MAX ACCELERATION:\t{} g'.format(maxes[2]/gravity)
    #plot
    ax = plt.axes()
    ax.plot(times, flight_data[:,0], color=(.4, 0.2, 1,1), label='Altitude')
    ax.plot(times, flight_data[:,1], color=(1, 0.2, 0.4,1), label='Velocity')
    ax.plot(times, flight_data[:,2], color=(.4, 1, 0.2,1), label='Acceleration')
    plt.legend()
    plt.xlabel('Time (s)')
    plt.ylabel('Meters (per s, s^2)')
    plt.title('Estimated p,v,a')
    plt.show()

