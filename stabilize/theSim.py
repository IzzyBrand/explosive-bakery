import numpy as np
from abc import abstractmethod
import time
import matplotlib.pyplot as plt

class E2:
	def __init__(self, x,y,theta):
		self.x = x
		self.y = y
		self.theta = theta

	def get_state(self):
		return np.array([self.x,self.y,self.theta])

class RocketComponent(object):
	def __init__(self, position, width, height, mass, name=None):
		self.width = width
		self.height = height
		self.cg = self.height/2
		self.mass = mass
		self.position = position
		self.name = name if name else "Unnamed"

	@abstractmethod
	def rotational_inertia(self):
		e = "Component class must have rot inertia method"
		raise NotImplementedError(e)

class RocketBody(RocketComponent):
	def __init__(self):
		super(RocketBody, self).__init__(0, .038, .7, .2, "body")

	# c_g is center of gravity, p is the center of the component
	def rotational_inertia(self, cg):
		w = self.width
		h = self.height
		py = self.position
		coeff = 1./12. * self.mass
		term1 = 4 * h**2 + w**2
		term2 = 12. * cg**2 + 12. * h * py
		term3 = 12. * py**2 - 12 * cg * (h + 2*py)
		return coeff * (term1 + term2 + term3)

	def __repr__(self):
		return '<rocket-component-%s>' % self.name

	def __str__(self):
		return 'component-%s' % self.name

class RocketFins(RocketComponent):
	def __init__(self):
		super(RocketFins, self).__init__(.7, .15, .075, .06, "fins")

	# cg is center of gravity, py distance from the top of the component
	# to the top of the rocket
	def rotational_inertia(self, cg):
		w = self.width
		h = self.height
		py = self.position
		coeff = 1./12. * h * w
		term1 = 4 * h**2 + w**2
		term2 = 12. * cg**2 + 12. * h * py
		term3 = 12. * py**2 - 12 * cg * (h + 2*py)
		return coeff * (term1 + term2 + term3)

	def __repr__(self):
		return '<rocket-component-%s>' % self.name

	def __str__(self):
		return 'component-%s' % self.name

class Rocket:
	def __init__(self, components):
		self.component_drag_coeff = .82
		self.component_lift_coeff = .6
		self.air_density = 1.225

		self.position = E2(0,0,np.pi/4)
		self.velocity = E2(50.,50.,0)

		self.components = components
		self.mass = 0
		cg_sum = 0

		for c in self.components:
			self.mass += c.mass
			cg_sum += c.mass * (c.position + c.cg)

		self.cg = cg_sum / self.mass
		self.rotational_inertia = 0
		for c in self.components:
			self.rotational_inertia += c.rotational_inertia(self.cg)

		print self.rotational_inertia

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
	fins = RocketFins()
	body = RocketBody()
	r = Rocket([fins, body])
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
