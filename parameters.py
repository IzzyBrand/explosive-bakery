from numpy import pi

##################### ROCKET PARAMETERS #####################
total_mass       = 1.6                   # kg     (bad approx)
rocket_length    = 0.18                  # m      (7 inch)
inner_diameter   = 0.025                 # m      (good)
outer_diameter   = 0.029                 # m      (?)
core_diameter    = 0.0051                # m      (?)
inner_radius     = inner_diameter / 2.0  # m
outer_radius     = outer_diameter / 2.0  # m
core_radius      = core_diameter  / 2.0  # m
drag_coefficient = 0.4                   # ()     (approx)
burn_rate        = 0.1                   # m/s    (bad approx)
fuel_density     = 400.0                  # kg/m^3 (bad approx)
fuel_mass        = pi * fuel_density * rocket_length * \
                    (inner_radius**2 - core_radius**2)

##################### PHYSICAL CONSTANTS ####################
G_constant      = 6.67408e-11  # m^3/(kg*s^2)
earth_mass      = 5.972e24     # kg
earth_radius    = 6.371e6      # m
temp_ground     = 288.15       # K
lapse_rate      = 0.0065       # m/s
pressure_ground = 101.325      # kPa
dry_MM          = 0.0289644    # kg/mol
ideal_gas_c     = 8.31447      # J/(mol * K)

#################### INITIAL CONDITIONS #####################
initial_time         = 0.0 # s
initial_height       = 0.0 # m (from sea level)
initial_velocity     = 0.0 # m/s
initial_acceleration = 0.0 # m/s^2

total_burn_time = (inner_radius - core_radius) / burn_rate # s
