import numpy as np

def actualImpulse(debris):
    impulse = np.zeros(3)
    for i in range(3):
        impulse[i] = np.sum(debris[:, 7] * debris[:, 8 + i])

    return impulse
