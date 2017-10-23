from numpy import pi, sqrt
import matplotlib.pyplot as plt
import numpy as np
from parameters import *
import time

times = []
pressures = []
burn_rates = []


def B(p):
    # input Pa
    # output burn rate (m/s)
    newp = (0.000145038 * p)
    br = (0.1494 * (newp ** 0.337)) / 100.
    return br

t = initial_time
dt = 1e-7 # seconds
pressure = pressure_ground # Pa
numerator   = 1 + ((k - 1) / 2 * M**2)
denominator = (1 + (k - 1) / 2)
exp         = -1 * ((k + 1) / (2 * (k - 1)))
exponent    = (k + 1) / (2 * (k - 1))
A_star      = nozzle_area #M * nozzle_area * (numerator / denominator) ** exp

R = R_effective
flag1 = False
flag2 = False
T_0 = burn_temp
ltime = time.time()
print '0.00%'
while core_radius <= inner_radius:
    if time.time() - ltime > 4:
        ltime = time.time()
        print '%s%%' % str(round(core_radius / inner_radius * 100, 2))
        
    burn_rate = B(pressure)
    core_radius += burn_rate * dt

    burn_area = 2 * pi * core_radius * motor_length
    chamber_volume = pi * core_radius ** 2 * motor_length

    gas_density = pressure / R / T_0
    burn_term = burn_rate * burn_area * (fuel_density - gas_density)
    
    exhaust_term = pressure * A_star * sqrt(k/(R*T_0)) * \
                   (2/(k+1))**exponent

    coeff = R * T_0 / chamber_volume
    dp = coeff * (burn_term - exhaust_term) * dt
    if dp < 0:
        print 'Warning: dpdt < 0 for pressure %s' % pressure
    pressure += dp
    t += dt

    burn_rates.append(burn_rate)
    times.append(t)
    pressures.append(pressure)

print 'Done.'

pressures = np.array(pressures)
plt.plot(times, 0.000145038 * pressures, label='Pressure')

# plt.plot(times, burn_rates,    label='BR')
plt.xlabel('Time (seconds)')
plt.ylabel('Pressure (psi)')
plt.legend()
plt.show()
