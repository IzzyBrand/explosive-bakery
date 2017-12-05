import numpy as np
import time
import matplotlib.pyplot as plt

class E2:
	def __init__(self, x,y,theta):
		self.x = x
		self.y = y
		self.theta = theta

	def get_state(self):
		return np.array([self.x,self.y,self.theta])

class RocketComponent:
	def __init__(self, position, width, height, mass):
		self.width = width
		self.height = height
		self.cg = self.height/2
		self.mass = mass
		self.position = position

class Rocket:
	def __init__(self):
		self.component_drag_coeff = .82
		self.component_lift_coeff = .6
		self.air_density = 1.225


		self.position = E2(0,0,np.pi/4)
		self.velocity = E2(50.,50.,0)

		tube = RocketComponent(0, .038, .7, .2)
		fins = RocketComponent(.7, .15, .15, .06)
		self.components = [tube,fins]
		self.mass = 0
		cg_sum = 0

		for c in self.components:
			self.mass += c.mass
			cg_sum += c.mass * (c.position + c.cg)

		self.cg = cg_sum/self.mass
		self.rotational_inertia = 0
		for c in self.components:
			self.rotational_inertia += c.mass/12. * (12*(c.position - self.cg)**2 + \
			 12*(c.position - self.cg) * c.height + 4 * c.height**2 + c.width**2)

	def step(self, dt):

		aoa =  np.arctan2(self.velocity.x, self.velocity.y) - self.position.theta 

		velocity2 = self.velocity.x**2 + self.velocity.y**2
		tot_lift = 0
		tot_drag = 0
		torque = 0

		for c in self.components:
			dist_to_cg = c.position + c.cg - self.cg
			force = c.width * c.height * velocity2 * self.air_density / 2.

			drag = - (np.sin(aoa) + .03) * force * self.component_drag_coeff
			lift = (np.sin(aoa) * np.cos(aoa) * force * self.component_lift_coeff)

			rotational_drag = - np.sign(self.velocity.theta) *(self.velocity.theta * dist_to_cg)**2 * c.width * c.height * self.air_density / 2. * self.component_drag_coeff

			tot_lift += lift
			tot_drag += drag
			torque += (drag * np.sin(aoa) + lift * np.cos(aoa)) * dist_to_cg + rotational_drag


		acceleration_x = np.sin(self.position.theta) * drag - np.cos(self.position.theta) * lift
		acceleration_y = np.cos(self.position.theta) * drag + np.sin(self.position.theta) * lift
		
		self.velocity.x += acceleration_x * dt
		self.velocity.y += (acceleration_y - 9.81) * dt
		self.velocity.theta += torque/self.rotational_inertia * dt

		self.position.x += self.velocity.x * dt
		self.position.y += self.velocity.y * dt
		self.position.theta += self.velocity.theta * dt

if __name__ == '__main__':
	r = Rocket()
	ps = []
	vs = []
	ts = []
	start_time = time.time()
	t = 0
	tt = t
	for i in range(50000):
		t = time.time() - start_time
		ts.append(t)
		dt = (t - tt)*5.
		r.step(dt)
		ps.append(r.position.get_state())
		vs.append(r.velocity.get_state())
		# print'%3f %3f %3f' % (r.velocity.x, r.velocity.y, r.position.theta)
		tt = t

	ps = np.array(ps)
	vs = np.array(vs)
	plt.plot(ts, ps[:,2], label='$\\theta$')
	plt.plot(ts, vs[:,0], label='$v_x$')
	plt.plot(ts, vs[:,1], label='$v_y$')
	plt.plot(ts, ps[:,1], label='$y$')
	plt.legend()
	plt.show()
