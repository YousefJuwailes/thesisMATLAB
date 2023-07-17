from DebrisGeneration.generateDebris import *
from DebrisGeneration.numberDebris import *
from DebrisGeneration.solveODExyz import *
from DebrisGeneration.collisionPoints import *


def runParameter(runs, ptCloud, dummyCloud, lowestPoint, projectileMass, projectileLength, projectileVelocity,
                 pointOfImpact, momentumConservationFactor, energyConservationFactor, c, b, minimumPenetrationDistance,
                 maximumPenetrationDistance, standardDeviation):
    # runParameter executes the simulation with the given parameters and returns the final positions of the debris.
    # dummyCloud and ptCloud must be variables in the workspace.

    N = numberDebris(projectileMass, np.linalg.norm(projectileVelocity), 0.05)
    storage = []

    storageDebris = []

    for n in range(runs):
        debris = generateDebris(projectileMass, projectileLength, projectileVelocity, pointOfImpact,
                                momentumConservationFactor, energyConservationFactor, c, b, minimumPenetrationDistance,
                                maximumPenetrationDistance, standardDeviation)

        storageDestinationsTemp = np.zeros((N, 3))

        for i in range(N):
            t, xyz = solveODExyz(debris[i, :], lowestPoint)
            destination = collisionPoints(xyz, ptCloud, dummyCloud, debris[i, 11])
            storageDestinationsTemp[i, :] = destination

        storage.append(storageDestinationsTemp)
        storageDebris = np.vstack((storageDebris, debris))

    storageDestinations = np.concatenate(storage)

    return storageDestinations, storageDebris
