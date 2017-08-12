from numpy import pi, sqrt
import numpy as np
from parameters import *

def gravity(h):
    return 9.807
    # return (G_constant * earth_mass) / ((earth_radius + h) ** 2)

def T_air(h):
    return temp_ground - lapse_rate * h

def B(p):
    # input PSI
    # output burn rate (cm/s)
    return 0.165 * (p ** 0.322)

def p_air(h):
    g = gravity(h)
    exponent = (g * dry_MM) / (ideal_gas_c * lapse_rate)
    base = (1 - (lapse_rate * h) / temp_ground)
    return pressure_ground * (base ** exponent)

def rho_air(h):
    return (p_air(h) * dry_MM) / (ideal_gas_c * T_air(h))

def v_sound(h):
    return 331.3 * sqrt(T_air(h) / 273.15)

def gamma(h):
    return pi / 2.0 * drag_coefficient * outer_radius ** 2 * rho_air(h)

def drag(v, h):
    return gamma(h) * v**2


# want p(t)


# def mass(t):
#     if t <= total_burn_time:
#         coeff      = pi * rocket_length * fuel_density * burn_rate
#         quadratic  = burn_rate * t**2 + 2.0 * core_radius * t
#         return total_mass - coeff * quadratic
#     else:
#         coeff   = pi * rocket_length * fuel_density
#         product = inner_radius ** 2 - core_radius ** 2
#         return total_mass - coeff * product

# def m_dot(t):
#     if t <= total_burn_time:
#         return -2.0 * pi * rocket_length * fuel_density * burn_rate * \
#                       (burn_rate * t + core_radius)
#     else:
#         return 0.0

def thrust(t):
    pass



