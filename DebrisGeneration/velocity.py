import math
import numpy as np

def generateDeltaVelocity(areaToMassRatio):
    # Generates velocities of debris using the NASA Breakup Model

    chi = math.log10(areaToMassRatio)
    mu = 0.9 * chi + 2.9
    # Original sigma
    sigma = 0.4

    # Attempted sigma
    # sigma = 0.2

    v = 10 ** np.random.normal(mu, sigma)

    u = np.random.uniform(-1, 1)
    theta = np.random.uniform(0, 2 * math.pi)

    velocity = [v * math.cos(theta) * (1 - u ** 2) ** (1 / 2), v * math.sin(theta) * (1 - u ** 2) ** (1 / 2), v * u]

    return velocity