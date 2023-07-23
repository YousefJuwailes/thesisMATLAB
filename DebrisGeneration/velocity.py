import math
import numpy as np

def generateDeltaVelocity(AM_ratio):
    chi = math.log10(AM_ratio)
    mu = 0.9 * chi + 2.9
    sigma = 0.4

    velMag = 10 ** np.random.normal(mu, sigma)

    u = np.random.uniform(-1, 1)
    theta = np.random.uniform(0, 2 * math.pi)
    velVec = np.array([
        velMag * math.cos(theta) * (1 - u ** 2) ** (1 / 2),
        velMag * math.sin(theta) * (1 - u ** 2) ** (1 / 2),
        velMag * u
    ])
    return velVec