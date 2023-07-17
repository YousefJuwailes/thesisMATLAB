def scaleDeltaVelocities(debris, projectileVelocity, scalingFactor):
    # debris has its mass in column 7 and its velocities from column 9 to 11
    debrisCorrected = debris.copy()
    debrisCorrected[:, 8:11] = (debrisCorrected[:, 8:11] - projectileVelocity) * scalingFactor + projectileVelocity

    return debrisCorrected
