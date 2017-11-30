import time

start_time = time.time()
in_string = raw_input()
print 'You entered {} after {} seconds.'.format(in_string, time.time() -start_time)
