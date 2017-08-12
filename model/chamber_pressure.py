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
    # input PSI
    # output burn rate (cm/s)
    return (0.165 * (p ** 0.322)) / 100.

t = initial_time
dt = 1e-4 # seconds
pressure = 14.6959 # PSI
numerator   = 1 + ((k - 1) / 2 * M**2)
denominator = (1 + (k - 1) / 2)
exp         = -1 * ((k + 1) / (2 * (k - 1)))
exponent = (k + 1) / (2 * (k - 1))
A_star      = M * nozzle_area * (numerator / denominator) ** exp
R = ideal_gas_c
T_0 = burn_temperature
k = 1.1
M = 1.0

# while core_radius <= inner_radius:
#     burn_rate = B(pressure)
#     core_radius += burn_rate * dt

#     chamber_volume = pi * core_radius ** 2 * rocket_length
#     # A* calculation
#     gas_density = pressure / R / T_0

#     burn_term    = R * T_0 * burn_rate / chamber_volume * \
#                    (fuel_density - gas_density)

#     A_b = pi * core_radius * 2 * rocket_length
    
#     exhaust_term = pressure * A_star * sqrt(k/(R*T_0)) * \
#                    (2/(k+1))**exponent

#     dpdt = burn_term - 0
#     dp = dpdt * dt
#     times.append(t)
#     pressures.append(pressure)
#     burn_rates.append(burn_rate)
#     burn_terms.append(burn_term)
#     exhaust_terms.append(exhaust_term)
#     pressure += dp
#     t += dt

plt.scatter(times, pressures,     label='Pressure')
# plt.plot(times, exhaust_terms, label='Exh')
# plt.plot(times, burn_terms,    label='Burn')
# plt.plot(times, burn_rates,    label='BR')
plt.legend()
plt.show()
