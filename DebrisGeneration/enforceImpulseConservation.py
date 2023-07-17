import numpy as np

def enforceImpulseConservation(debris, projectileVelocity, projectileMass, factor):
    # debris has its mass in column 6 and its velocities from column 8 to 10

    # calculate original Impulse
    originalImpulse = np.zeros(3)
    originalImpulse[0] = projectileVelocity[0] * projectileMass
    originalImpulse[1] = projectileVelocity[1] * projectileMass
    originalImpulse[2] = projectileVelocity[2] * projectileMass

    # calculate actual Impulse
    actualImpulse = np.zeros(3)
    for i in range(3):
        actualImpulse[i] = np.sum(debris[:, 7] * debris[:, 8 + i])

    velocityCorrection = (originalImpulse * factor - actualImpulse) / projectileMass
    impulseCorrection = velocityCorrection * projectileMass

    debris[:, 8] += velocityCorrection[0]
    debris[:, 9] += velocityCorrection[1]
    debris[:, 10] += velocityCorrection[2]

    return debris
