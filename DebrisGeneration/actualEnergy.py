import numpy as np

def actualEnergy(debris):
    N = debris.shape[0]
    actualEnergy = 0

    for i in range(N):
        actualEnergy += 1 / 2 * debris[i, 7] * np.linalg.norm(debris[i, 8:11]) ** 2

    energy = actualEnergy
    return energy
