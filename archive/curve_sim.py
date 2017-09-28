import numpy as np

def burn_rate_from_pressure(pressure):
    """ takes a pressure in atmospheres and returns a burn rate in inches per second"""
    return 0.377418 + np.log(0.02683)

#############################################
#                   CONFIG                  #
#############################################

# rocket geometery
core_diameter = 0.25
diameter = 1.0
length = 7
nozzle_diameter = 0.3125

# fuel parameters
propellant_density = 1.0

# simulation paramters
t_step = 0.001
t_max

pressure = 0

if __name__ == '__main__':
    core_radius = core_diameter/2.0
    t = 0
    instantaneous_gas_density = 1.2041 # density of air at 20C

    while True:
        burning_area = core_radius * 2.0 * np.pi * length
        burn_rate = burn_rate_from_pressure(pressure)

        # trying to implement this: https://www.nakka-rocketry.net/th_pres.html

        combustion_product_production_rate = burning_area * burn_rate * propellant_density

        instantaneous_gas_volume = (core_radius)**2 * np.pi * length

        changing_gas_volume = burning_area * burn_rate

        mass_storage_rate =  changing_gas_volume * instantaneous_gas_density + instantaneous_gas_volume * changing_gas_density

        
        
        # mass_outflow = P0 * A * np.sqrt(k/(R * T0)) * (2 / (k+1))**((k+1)/(2*k - 2)) # ???? shit has gone to shit

        # mass_storage_rate = mass_generation - mass_outflow


        if core_radius * 2.0 < diameter: core_radius += burn_rate * t_step
        t += t_step