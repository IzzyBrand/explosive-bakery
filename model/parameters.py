from numpy import pi

#################### ROCKET PARAMETERS ####################
total_mass       = 1.0                   # kg     (bad approx)
drag_coefficient = 0.4                   # ()     (approx)
surface_area	 = 0.002				 # m^2	  (bad approx)

##################### MOTOR PARAMETERS #####################

motor_length    = 0.18                   # m      (7 inch)
inner_diameter  = 0.025                  # m      (good)
outer_diameter  = 0.029                  # m      (?)
core_diameter   = 0.005                  # m      (?)
inner_radius    = inner_diameter / 2.0   # m
outer_radius    = outer_diameter / 2.0   # m
core_radius     = core_diameter  / 2.0   # m
fuel_density    = 1887.7695              # kg/m^3
burn_temp       = 1720                   # K
nozzle_diameter = 0.0063                 # m
inlet_area      = inner_radius ** 2 * pi # m
outlet_area     = inlet_area             # m

nozzle_area      = pi * (nozzle_diameter / 2)**2
fuel_mass        = pi * fuel_density * motor_length * \
                    (inner_radius**2 - core_radius**2)

##################### PHYSICAL CONSTANTS ####################
G_constant      = 6.67408e-11  # m^3/(kg*s^2)
earth_mass      = 5.972e24     # kg
earth_radius    = 6.371e6      # m
temp_ground     = 288.15       # K
lapse_rate      = 0.0065       # m/s
pressure_ground = 101325.0     # Pa
dry_MM          = 0.0289644    # kg/mol
ideal_gas_c     = 8.31447      # J/(mol * K)
air_density     = 1.225 	   # kg/m^2
gravity	    	= 9.81         # m/s^2

#################### INITIAL CONDITIONS #####################
initial_time         = 0.0 # s
initial_height       = 0.0 # m (from sea level)
initial_velocity     = 0.0 # m/s
initial_acceleration = 0.0 # m/s^2

k = 1.1331 # source http://www.nakka-rocketry.net/techs.html
M = 0.04198  # kg / mol
R_effective = ideal_gas_c / M
