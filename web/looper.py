import sys
import signal
import time

x = 0
while True:
    try:
        x += 1
        time.sleep(0.01)
    except KeyboardInterrupt:
        f = open('/tmp/hi.txt', 'w')
        f.write('%s' % x)
        f.flush()
        f.close()
        sys.exit(0)

