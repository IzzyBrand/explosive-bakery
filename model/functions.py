from sdebe import SDEBE

def burn_rate(P):
    # input PSI
    # output m/s
    return (0.165 * (p ** 0.322)) / 100.

def f(y, t):
    P           = y[0]
    radius      = y[1]
    outer_coeff = R * T / vol
    rho_p       = P / (R * T)
    del_rho     = rho_p - rho_0
    term1       = None

def jac(y, t):
    jacobian = np.zeros((2, 2))
    jacobian[0,0] = 

def G(y, t):
    return np.zeros((2, 2))

sde = SDEBE(f, G)
sde.integrate(0, )

