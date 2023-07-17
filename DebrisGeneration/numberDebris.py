def numberDebris(massProjectile, velocityProjectile, smallestDebrisSize):
    # Returns the number of debris pieces based on the mass and velocity of the projectile.

    # Parameter to adjust the number
    s = 2.2138e-5

    n = round(s * (massProjectile * velocityProjectile) ** 0.75 / smallestDebrisSize ** 1.71)

    return n