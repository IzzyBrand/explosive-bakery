# Handle all logging on Carlson flight computer. This includes sensor data and 
# video captured on the Pi camera.
#
# Note: this code uses the picamera module which must be run on a Raspberry Pi.
#
# Benjamin Shanahan & Elias Berkowitz

import os
import time
from picamera import PiCamera
from datetime import datetime

# Define directories (include terminating forward-slash!)
ROOT      = "/home/pi/explosive-bakery/carlson2/"
LOG_DIR   = ROOT + "log/"
VIDEO_DIR = ROOT + "video/"
EXT       = "csv"
VIDEO_EXT = "h264"

# Video-specific parameters
CAPTURE_RES = (1920, 1080)  # in pixels

class Logger:

    def __init__(self, init_logfile=True, init_camera=True):
        self.file           = None
        self.filename       = None
        self.camera         = None
        self.camera_enabled = False
        if init_logfile: self._init_new_logfile()
        if init_camera:  self._init_camera()

    def start_video(self):
        if self.camera_enabled: 
            self.camera.start_recording(VIDEO_DIR + self.filename + "." + VIDEO_EXT)
            print "Started video capture."

    def stop_video(self):
        if self.camera_enabled:
            self.camera.stop_recording()
            print "Stopped video capture."

    # Write data to file. Data is specified as a list, and delimeter is used
    # to separate each data point when written. If flush is True, this function
    # immediately flushes the written data to file as well.
    def write(self, data, delimeter=",", flush=True):
        # Append each element in data list to a string
        log_str = ""
        n       = len(data)
        for idx, val in enumerate(data):
            log_str += ("%s" % val)
            # Add delimeter or newline to end of string
            if idx == (n-1):
                log_str += "\n"
            else:
                log_str += delimeter + "\t"

        # Write to file and flush (if specified)
        self.file.write(log_str)
        if flush: self.file.flush()

    # Stop logger. This consists of closing the open file descriptor and 
    # stopping our video stream.
    def stop_all(self):
        # Flush and close file
        self.file.flush()
        self.file.close()

        # Stop video capture
        self.stop_video()
    
    def _init_new_logfile(self):
        # For every file in the log directory ending with EXT extension, we 
        # parse the number at the start of the filename, and if it is larger
        # than the number we have saved in last_launch, we update last_launch
        # to this new value.
        last_launch = 0
        for f in [x for x in os.listdir(LOG_DIR) if x.endswith(EXT)]:
            try:
                launch_numb = int(f.split("_")[0])  # get number at start of file
                last_launch = launch_numb if launch_numb > last_launch else last_launch
            except ValueError:
                print "Warning: Invalid .%s file in logs folder (%s)" % (EXT, f)
                return False

        # Next, we generate a new filename based of the current system time.
        # The now() function returns the system time, and on the Raspberry Pi, 
        # without internet connection, this function will return the date from
        # last internet contact (i.e. this date will be wrong most of the 
        # time unless you connect to WiFi).
        date          = datetime.now().strftime("%y-%m-%d")
        self.filename = "%03d_%s" % (last_launch + 1, date)

        # Generate the full save path and verify that this file does not 
        # already exist.
        fullpath = "%s%s.%s" % (LOG_DIR, self.filename, EXT)
        if os.path.exists(fullpath):
            print "Error: Log file already exists (%s)" % fullpath
            return False
            
        # Get a file descriptor for the new file
        self.file = open("%s%s.%s" % (LOG_DIR, self.filename, EXT), "a")
        print "Created log file (%s.%s)." % (self.filename, EXT)
        return True

    # Configure camera on the Pi
    def _init_camera(self):
        try:
            self.camera = PiCamera()
            self.camera.resolution = CAPTURE_RES
            self.camera_enabled = True
            print "Initialized camera to capture at %d*%d px." % CAPTURE_RES
        except:
            self.camera_enabled = False
            print "Failed to initialize camera."