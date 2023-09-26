from DebrisGeneration.generateDebris import *
from DebrisGeneration.numberDebris import *
from DebrisGeneration.solveODExyz import *
from DebrisGeneration.collisionPoints import *


def runParameter(ptCloud, lowestPoint, projectileMass, projectileLength, projectileVelocity,
                 pointOfImpact, psi, phi, c, b, minimumPenetrationDistance,
                 maximumPenetrationDistance, standardDeviation):
    
    # runParameter executes the simulation with the given parameters and returns the final positions of the debris.
    # dummyCloud and ptCloud must be variables in the workspace.

    N = numberDebris(projectileMass, np.linalg.norm(projectileVelocity), 0.05)
    debris = generateDebris(projectileMass, projectileLength, projectileVelocity, pointOfImpact,
                            psi, phi, c, b, minimumPenetrationDistance,
                            maximumPenetrationDistance, standardDeviation, N)

    destinations = np.zeros((N, 3))
    for i in range(N):
        t, xyz = solveODExyz(debris[i, :], lowestPoint)
        destinations[i, :] = collisionPoints(xyz, ptCloud, debris[i, 11], ptCloud)

    return destinations