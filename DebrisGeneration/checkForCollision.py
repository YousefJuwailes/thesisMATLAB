from scipy.spatial import cKDTree

def checkForCollision(position, elevation, elevationZero):
    # Create a KD tree from the elevationZero coordinates
    kd_tree = cKDTree(elevationZero[:, :2])  # Only consider x and y coordinates

    # Find the nearest neighbor index
    _, index = kd_tree.query(position[:2], k=1)

    if position[2] < elevation[index, 2]:
        collision = 1
    else:
        collision = 0

    return collision