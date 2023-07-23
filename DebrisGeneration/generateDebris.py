from .numberDebris import *
from .generateMissingPiece import *
from .generateRandomPiece import *

from .scaleDeltaVelocities import *
from .enforceImpulseConservation import *
from .actualEnergy import *
from .velocity import *
from .penetration import *

def generateDebris(projectileMass, projectileLength, projectileVelocity, pointOfImpact,
                   psi, phi, c, b, minP, maxP, devP, N):
    # Generates an array of debris. Each row represents a piece of debris with coordinates, a characteristic length,
    # an area-to-mass ratio, mass, area, CW value, and velocity magnitude in coordinate direction.

    numberOfParameters = 12

    absoluteProjectileVelocity = np.linalg.norm(projectileVelocity)

    Debris = np.zeros((N, numberOfParameters))
    for i in range(N):
        Debris[i, 0:3] = pointOfImpact
        Debris[i, 3] = generateCharacteristicLength(0.05, projectileLength)   # Lc
        Debris[i, 4] = areaToMassRatio(Debris[i, 3])                                        # A/m
        Debris[i, 5] = surfaceAreaDebris(Debris[i, 3], c, b)                                # Ac
        Debris[i, 6] = mass(Debris[i, 5], Debris[i, 4], c)                                  # m
        Debris[i, 7] = cw()                                                                 # Cw

    # Mass conservation
    # Generate missing pieces if necessary
    totalMass = np.sum(Debris[:, 6])
    if totalMass < projectileMass:
        Debris = np.delete(Debris, N, axis=0)
        missingPiece = generateMissingPiece(projectileMass - totalMass, generateCharacteristicLength(0.05, projectileLength), numberOfParameters)
        Debris = np.concatenate((Debris, missingPiece), axis=0)

    # Ensure no piece weighs more than 10% of the total mass
    tooHeavy = True
    while tooHeavy:
        m, i = np.max(Debris[:, 6]), np.argmax(Debris[:, 6])
        if m >= 0.1 * projectileMass:
            Debris = np.delete(Debris, i, axis=0)
            newPiece = generateRandomPiece(pointOfImpact, projectileLength, 0.05, numberOfParameters, c, b)
            Debris = np.concatenate((Debris, newPiece), axis=0)
        else:
            tooHeavy = False

    # Scale the weight of the pieces
    totalMass = np.sum(Debris[:, 6])
    factor = projectileMass / totalMass
    Debris[:, 6] *= factor                      # scale mass
    Debris[:, 4] = Debris[:, 5] / Debris[:, 6]  # new A/m

    # velocity assignment
    for i in range(N):
        vel = generateDeltaVelocity(Debris[i, 4])
        Debris[i, 8] += vel[0]
        Debris[i, 9] += vel[1]
        Debris[i, 10] += vel[2]

    # Generate penetration capabilities
    maxMass = np.max(Debris[:, 6])
    minMass = np.min(Debris[:, 6])
    for i in range(N):
        mean = lambda x: (minP - maxP) / (maxMass - minMass) * (x - minMass) + minP
        Debris[i, 11] = np.random.normal(mean(Debris[i, 6]), devP)
        if Debris[i, 11] < 0:
            Debris[i, 11] = 0

    debrisMomentum  = np.array([0, 0, 0])
    planeMomentum   = np.array([0, 0, 0])
    planeMomentum[0]   = projectileMass * projectileVelocity[0]
    planeMomentum[1]   = projectileMass * projectileVelocity[1]
    planeMomentum[2]   = projectileMass * projectileVelocity[2]
    debrisMomentum, Debris = conserveMomentum(Debris, debrisMomentum, planeMomentum, psi, projectileMass)
    Debris  = pseudoConservation(Debris, debrisMomentum, planeMomentum, psi, projectileMass, phi, projectileVelocity)

    return Debris

def pseudoConservation(Debris, debrisMomentum, planeMomentum, psi, planeMass, phi, planeVelVec):
    planeKE = 0.5 * planeMass * np.linalg.norm(planeVelVec)**2
    for i in range(2, 100):
        debrisKE   = 0
        for i in range(len(Debris)):
            debrisKE += 0.5 * Debris[i, 6] * np.linalg.norm(Debris[i, 8:11])**2 

        if debrisKE > planeKE * phi:
                for j in range(len(Debris)):
                    Debris[j, 8]    = (Debris[j, 8] - planeVelVec[0])*(1 - (1/i)) + planeVelVec[0]
                    Debris[j, 9]    = (Debris[j, 9] - planeVelVec[1])*(1 - (1/i)) + planeVelVec[1]
                    Debris[j, 10]   = (Debris[j, 10] - planeVelVec[2])*(1 - (1/i)) + planeVelVec[2]
        else:
            for j in range(len(Debris)):
                Debris[j, 8]    = (Debris[j, 8] - planeVelVec[0])*(1 + (1/i)) + planeVelVec[0]
                Debris[j, 9]    = (Debris[j, 9] - planeVelVec[1])*(1 + (1/i)) + planeVelVec[1]
                Debris[j, 10]   = (Debris[j, 10] - planeVelVec[2])*(1 + (1/i)) + planeVelVec[2]
            
        debrisMomentum, Debris = conserveMomentum(Debris, debrisMomentum, planeMomentum, psi, planeMass)

    if debrisKE > phi*planeKE: 
        pseudoConservation(Debris, debrisMomentum, planeMomentum, psi, planeMass, phi, planeVelVec)

    flage = 1
    return Debris


def conserveMomentum(Debris, debrisMomentum, planeMomentum, psi, planeMass):
    debrisMomentum[0]  = np.sum(Debris[:, 6] * Debris[:, 8])
    debrisMomentum[1]  = np.sum(Debris[:, 6] * Debris[:, 9])
    debrisMomentum[2]  = np.sum(Debris[:, 6] * Debris[:, 10])
    deltaV = (planeMomentum * psi - debrisMomentum)/planeMass
    for i in range(len(Debris)):
        Debris[i, 8]    += deltaV[0]
        Debris[i, 9]    += deltaV[1]
        Debris[i, 10]   += deltaV[2]

    return debrisMomentum, Debris 
