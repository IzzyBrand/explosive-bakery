import numpy as np

class E2:
	def __init__(self, x,y,theta):
		self.x = x
		self.y = y
		self.theta = theta

class RocketComponent:
	def __init__(self, position, width, height, mass):
		self.width = width
		self.height = height
		self.cg = self.height/2
		self.mass = mass
		self.position = position

class Rocket:
	def __init__(self):
		self.position = E2(0,0,0)
		self.velocity = E2(0,0,0)
		tube = RocketComponent(0, .038, .7, .2)
		fins = RocketComponent(.7, .15, .15, .06)
		self.components = [tube,fins]
		self.mass = 0
		cg_sum = 0
		
		for component in self.components:
			self.mass += component.mass
			cg_sum += component.mass * (component.position + component.cg)

		self.cg = cg_sum/self.mass
		self.rotational_inertia = 0
		for c in self.components:
			self.rotational_inertia += c.mass/12. * (12*(c.position - self.cg)**2 + \
			 12*(c.position - self.cg) * c.height + 4 * c.height**2 + c.width**2)

	def step(self, dt):
		self.position.x += self.velocity.x * dt
		self.position.y += self.velocity.y * dt


if __name__ == '__main__':
	r = Rocket()


