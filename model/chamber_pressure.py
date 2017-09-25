from numpy import pi, sqrt
import matplotlib.pyplot as plt
import numpy as np
from parameters import *


times = []
pressures = []
burn_terms = []
exhaust_terms = []
burn_rates = []


def B(p):
    # input N/m^2
    # output burn rate (m/s)
    newp = (14.6959488 * p)
    print newp
    br = (0.1494 * (newp ** 0.337)) / 100.
    print br
    return br

t = initial_time
dt = 1e-5 # seconds
pressure = 1. # N/m^2
numerator   = 1 + ((k - 1) / 2 * M**2)
denominator = (1 + (k - 1) / 2)
exp         = -1 * ((k + 1) / (2 * (k - 1)))
exponent = (k + 1) / (2 * (k - 1))
A_star      = M * nozzle_area * (numerator / denominator) ** exp

R = R_effective
flag1 = False
flag2 = False
T_0 = burn_temperature
while core_radius <= inner_radius:
    if not flag1 and core_radius >= inner_radius / 2:
        flag1 = True
        print '1/2 done'

    if not flag2 and core_radius >= 3*inner_radius / 4:
        flag2 = True
        print '3/4 done'
        
    burn_rate = B(pressure)
    core_radius += burn_rate * dt

    burn_area = 2 * pi * core_radius * motor_length
    chamber_volume = pi * core_radius ** 2 * motor_length

    gas_density = pressure / R / T_0
    burn_term = burn_rate * burn_area * (fuel_density - gas_density)
    
    exhaust_term = pressure * A_star * sqrt(k/(R*T_0)) * \
                   (2/(k+1))**exponent

    coeff = R * T_0 / chamber_volume
    dpdt = coeff * (burn_term - exhaust_term)
    dp = dpdt * dt
    times.append(t)
    pressures.append(pressure)
    burn_rates.append(burn_rate)
    burn_terms.append(burn_term)
    exhaust_terms.append(exhaust_term)
    pressure += dp
    t += dt

print np.size(pressures)
plt.plot(times, pressures,     label='Pressure')
# plt.plot(times, exhaust_terms, label='Exh')
# plt.plot(times, burn_terms,    label='Burn')
# plt.plot(times, burn_rates,    label='BR')
plt.legend()
plt.show()
