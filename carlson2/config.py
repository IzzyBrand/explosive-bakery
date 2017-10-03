import struct

###############################################################################
## Sensors and IO
###############################################################################

RTIMU_calibration_file = "RTIMULib"
chute_pin              = 4
blast_cap_burn_time    = 5

###############################################################################
## Telemetry
###############################################################################

port                = "/dev/ttyUSB0"
baud                = 57600
serial_timeout      = 0
time_before_resend  = 0.5  # (s) how long to wait before panicking (send again)
heartbeat_delay     = 1    # (s) delay between heartbeats
heartbeat_max_delay = 3    # (s) max delay between heartbeats before panic

# Telemetry commands
HEARTBEAT = "H"
ARM       = "a"
DEPLOY    = "d"
STOP      = "x"
HELP      = "h"
QUIT      = "q"
NOPE      = "0"  # I got your command, but I'm not executing it

###############################################################################
## Data Logging + Video
###############################################################################

log_folder   = "logs"
video_folder = "videos"
capture_res  = (1920, 1080)  # in pixels