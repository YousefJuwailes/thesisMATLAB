def meanPenetrationDistance(minMass, maxMass, minDistance, maxDistance):
    # Returns a function that calculates the average penetration distance of debris
    # considering its own mass, as well as the mass of the lightest and heaviest particle.

    f = lambda x: (maxDistance - minDistance) / (maxMass - minMass) * (x - minMass) + minDistance
    return f
