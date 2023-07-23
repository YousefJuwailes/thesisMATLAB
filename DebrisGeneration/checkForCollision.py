from scipy.spatial import cKDTree

def checkForCollision(position, elevation, KDTree):
    # Find the nearest neighbor index
    _, index = KDTree.query(position[:2], k=1)
    if position[2] < elevation[index, 2]:
        collision = 1
    else:
        collision = 0

    return collision