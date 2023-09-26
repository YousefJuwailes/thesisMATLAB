from scipy.spatial  import cKDTree
import numpy        as np
import laspy


def checkForCollision(position, elevation, ptCloud):
    KDTree = cKDTree(ptCloud[:, :2])

# Find the nearest neighbor index
    _, index = KDTree.query(position[:2], k=1)
    if position[2] < elevation[index, 2]:
        collision = 1
    else:
        collision = 0

    return collision