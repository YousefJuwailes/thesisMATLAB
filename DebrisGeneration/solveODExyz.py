import numpy as np
from scipy.integrate import odeint


def odefcnxyz(y, t, m, Cw, A, rho, g):
    dydt = np.zeros(6)
    v = np.sqrt(y[3] ** 2 + y[4] ** 2 + y[5] ** 2)
    mu = Cw * A * rho / (2 * m)
    dydt[0] = y[3]
    dydt[1] = y[4]
    dydt[2] = y[5]
    dydt[3] = -mu * y[3] * v
    dydt[4] = -mu * y[4] * v
    dydt[5] = -g - mu * y[5] * v
    return dydt


def solveODExyz(particle, deepestPoint):
    # SOLVEODEXYZ solves for the trajectory of one piece of debris

    # Surface area
    A = particle[6]
    # Aerodynamic drag coefficient
    Cw = particle[8]
    # Particle mass
    m = particle[7]

    # Air density at laboratory conditions in kg/m^3 (Wikipedia)
    rho = 1.2041
    # Gravitational acceleration factor in m/s^2 (Wikipedia)
    g = 9.8067

    y0 = np.concatenate((particle[:3], particle[9:12]))

    # Solve approximately to estimate the time interval and find the time interval with the deepest point
    opts = {"atol": 1e-6, "rtol": 1e-6}
    doLoop = True
    time = 5
    t1 = 0
    while doLoop:
        tspan = np.array([0, time])
        t = np.linspace(tspan[0], tspan[1], num=1000)
        xyz = odeint(odefcnxyz, y0, t, args=(m, Cw, A, rho, g), **opts)
        if xyz[-1, 2] < deepestPoint:
            doLoop = False
        else:
            time *= 2

    for i in range(0, len(t), 10):
        if xyz[i, 2] < deepestPoint:
            t1 = t[i] + 0.5
            break

    # Solve more accurately
    tspan = np.array([0, t1])
    t = np.linspace(tspan[0], tspan[1], num=10000)
    xyz = odeint(odefcnxyz, y0, t, args=(m, Cw, A, rho, g), **opts)

    return t, xyz
