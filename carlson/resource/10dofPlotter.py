import numpy as np
import matplotlib.pyplot as plt
import sys

f = open(sys.argv[1])
data = []
for line in f.read().split('\n')[0:-1]:
	data.append(map(float, line.split(',\t')))

bdata = np.array(data)
start = 1500
end = 5000
times = bdata[start:end,0]


plt.scatter(times, bdata[start:end, 1], label='state', s=6, c='purple')
plt.scatter(times, bdata[start:end, 2], label='state', s=6, c=(1,0,0))
plt.scatter(times, bdata[start:end, 3], label='state', s=6, c=(.75,0,0))
plt.scatter(times, bdata[start:end, 4], label='state', s=6, c=(.5,0,0))
plt.scatter(times, bdata[start:end, 5], label='state', s=6, c=(0,1,0))
plt.scatter(times, bdata[start:end, 6], label='state', s=6, c=(0,.75,0))
plt.scatter(times, bdata[start:end, 7], label='state', s=6, c=(0,.5,0))
plt.scatter(times, bdata[start:end, 8], label='state', s=6, c=(0,0,1))
plt.scatter(times, bdata[start:end, 9], label='state', s=6, c=(0,0,.75))
plt.scatter(times, bdata[start:end, 10], label='state', s=6, c=(0,0,.5))

for i in range(5, 11):
	if i >= 8:
		c = 'b'
	else:
		c = 'r'
	plt.scatter(times, bdata[start:end, 5], label='%ith column' % i, s=6,c=c)

# plt.legend()
plt.show()