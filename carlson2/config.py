class State:

    ###############################################################################
    ## Rocket States
    ###############################################################################

    IDLE              = 0    # default state on rocket boot

    ARM               = 1    # arm / disarm rocket and allow other functionality
    ARM_BIT           = 0    # bit position

    RECORD_DATA       = 2    # start / stop recording sensor data to disk
    RECORD_DATA_BIT   = 1 

    RECORD_VIDEO      = 4    # start / stop camera capture
    RECORD_VIDEO_BIT  = 2

    DEPLOY_CHUTE      = 8    # toggle parachute GPIO pin
    DEPLOY_CHUTE_BIT  = 3

    POWER_OFF         = 16   # shut down computer (last possible state)
    POWER_OFF_BIT     = 4 

    # Retrieve value of bit at index in given byte. Return True if bit is 1.
    @staticmethod
    def get_bit(byte_val, idx):
        return ((byte_val & (1 << idx)) != 0);

###############################################################################
## Sensors and IO
###############################################################################

class Sensor:

    RTIMU_INI_FILE      = "RTIMULib"
    CHUTE_PIN           = 4
    BLAST_CAP_BURN_TIME = 3  # seconds

###############################################################################
## Telemetry
###############################################################################

class Telemetry:

    PORT                = "/dev/ttyUSB0"
    BAUD                = 57600
    SERIAL_TIMEOUT      = 0
    TIME_BEFORE_RESEND  = 0.5  # (s) how long to wait before panicking (send again)
    HEARTBEAT_DELAY     = 1    # (s) delay between heartbeats
    HEARTBEAT_MAX_DELAY = 3    # (s) max delay between heartbeats before panic

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

class Logging:

    LOG_FOLDER   = "logs"
    VIDEO_FOLDER = "videos"
    CAPTURE_RES  = (1920, 1080)  # in pixels