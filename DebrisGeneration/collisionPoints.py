import numpy as np
from .checkForCollision import *

def collisionPoints(xyz, elevation, penetrationDistance, KDTree):
    # COLLISIONPOINTS returns the final destination for a given particle trajectory and the elevation model

    destination = [0, 0, 0]
    j = 0

    # missedDestination = []

    for i in range(0, xyz.shape[0], 10):
        if checkForCollision(xyz[i, :3], elevation, KDTree) and np.linalg.norm(
                xyz[i, :3] - xyz[0, :3]) > penetrationDistance:
            destination = xyz[i, :3]
            j = i
            break

    if j >= 9:
        for i in range(1, 10):
            if checkForCollision(xyz[j - i, :3], elevation, KDTree):
                destination = xyz[j - i, :3]

    return destination
