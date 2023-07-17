import numpy as np
from scipy.integrate import odeint


def odefcnxy(y, t, m, Cw, A, rho):
    dydt = np.zeros(2)
    dydt[0] = y[1]
    dydt[1] = -1 / (m * 2) * Cw * A * rho * y[1] ** 2
    return dydt


def solveODExy():
    # SOLVEODE Solves for the trajectory of one piece of debris in x- or y-direction

    A = 1
    Cw = 1
    rho = 1
    g = 10
    alpha = 1
    phi = 1

    m = 10

    tspan = [0, 20]
    y0 = [0, 10]

    t = np.linspace(tspan[0], tspan[1], num=1000)
    y = odeint(odefcnxy, y0, t, args=(m, Cw, A, rho))

    return t, y
