from .numberDebris import *
from .generateMissingPiece import *
from .generateRandomPiece import *

from .scaleDeltaVelocities import *
from .enforceImpulseConservation import *
from .actualEnergy import *
from .velocity import *
from .penetration import *

def generateDebris(projectileMass, projectileLength, projectileVelocity, pointOfImpact,
                   impulseConservationFactor, energyConservationFactor, c, b, minimumPenetrationDistance,
                   maximumPenetrationDistance, standardDeviation):
    # Generates an array of debris. Each row represents a piece of debris with coordinates, a characteristic length,
    # an area-to-mass ratio, mass, area, CW value, and velocity magnitude in coordinate direction.

    numberOfParameters = 12

    projectileVelocityX = projectileVelocity[0]
    projectileVelocityY = projectileVelocity[1]
    projectileVelocityZ = projectileVelocity[2]

    absoluteProjectileVelocity = np.linalg.norm(projectileVelocity)

    # Consider debris larger than 5cm, adjust if necessary.
    smallestDebrisSize = 0.05
    N = numberDebris(projectileMass, absoluteProjectileVelocity, smallestDebrisSize)

    Debris = np.zeros((N, numberOfParameters))

    for i in range(N):
        # Set position
        Debris[i, 0:3] = pointOfImpact

        # Set characteristic length
        Debris[i, 3] = generateCharacteristicLength(smallestDebrisSize, projectileLength)

        # Area-to-Mass Ratio
        Debris[i, 4] = areaToMassRatio(Debris[i, 3])

        # Surface Area
        Debris[i, 5] = surfaceAreaDebris(Debris[i, 3], c, b)

        # Mass
        Debris[i, 6] = mass(Debris[i, 5], Debris[i, 4], c)

        # CW value
        Debris[i, 7] = cw()

    Mass = np.sort(Debris[:, 6], axis=0)[::-1]

    # Ensure mass conservation
    totalMass = np.sum(Debris[:, 6])

    # Generate missing pieces if necessary
    if totalMass < projectileMass:
        Debris = np.delete(Debris, N, axis=0)
        missingPiece = generateMissingPiece(projectileMass - totalMass, generateCharacteristicLength(smallestDebrisSize, projectileLength), numberOfParameters)
        Debris = np.concatenate((Debris, missingPiece), axis=0)

    # Ensure no piece weighs more than 10% of the total mass
    tooHeavy = True
    while tooHeavy:
        m, i = np.max(Debris[:, 6]), np.argmax(Debris[:, 6])
        if m >= 0.1 * projectileMass:
            Debris = np.delete(Debris, i, axis=0)
            newPiece = generateRandomPiece(pointOfImpact, projectileLength, smallestDebrisSize, numberOfParameters, c, b)
            Debris = np.concatenate((Debris, newPiece), axis=0)
        else:
            tooHeavy = False

    # Scale the weight of the pieces
    totalMass = np.sum(Debris[:, 6])
    factor = projectileMass / totalMass

    # Scale mass
    Debris[:, 6] *= factor

    # Adjust Area-to-Mass Ratio
    Debris[:, 4] = Debris[:, 5] / Debris[:, 6]


    numberOfDebris = Debris.shape[0]
    for i in range(numberOfDebris):
        vel = generateDeltaVelocity(Debris[i, 4])

        Debris[i, 8] += vel[0]/10
        Debris[i, 9] += vel[1]/10
        Debris[i, 10] += vel[2]/10

    originalEnergy = 1/2 * projectileMass * np.linalg.norm(projectileVelocity) ** 2

    # Generate penetration capabilities
    maximumWeight = np.max(Debris[:, 6])
    minimumWeight = np.min(Debris[:, 6])

    meanDistance = meanPenetrationDistance(minimumWeight, maximumWeight, minimumPenetrationDistance, maximumPenetrationDistance)

    for i in range(N):
        Debris[i, 11] = np.random.normal(0, standardDeviation) + meanDistance(Debris[i, 6])
        if Debris[i, 11] < 0:
            Debris[i, 11] = 0

    Debris = enforceImpulseConservation(Debris, projectileVelocity, projectileMass, impulseConservationFactor)

    for i in range(2, 100):
        if actualEnergy(Debris) > originalEnergy * energyConservationFactor:
            Debris = scaleDeltaVelocities(Debris, projectileVelocity, 1 - (1/i))
        else:
            Debris = scaleDeltaVelocities(Debris, projectileVelocity, 1 + (1/i))
        Debris = enforceImpulseConservation(Debris, projectileVelocity, projectileMass, impulseConservationFactor)

    return Debris

