import sys
import os
import signal
import time

path = sys.argv[1]
xs = []
start = time.time()
x = 0
while True:
    try:
        x += 1
        xs.append([time.time() - start, x])
        time.sleep(0.01)
    except KeyboardInterrupt:
        f = open(os.path.join(path, 'log.txt'), 'w')
        f.write('%s' % '\n'.join(map(lambda s: '%s, %s' % (s[0], s[1]), xs)))
        f.flush()
        f.close()
        sys.exit(0)

