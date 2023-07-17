from runParameter import *
from showDestinations import *

lowestPoint = 190

# Point of Impact (House Number 128)
pointOfImpact = [371468.11, 5672127.86, 290]

# Course after bouncing off the house
course = 167.54

# Inverted Sink Rate
sinkRate = -58
velocity = 144
scalingFactor = (velocity**2 - sinkRate**2)**0.5

# How many times the entire simulation is run
runs = 50

projectileMass = 11726.27
projectileVelocity = [np.sin(np.radians(course)) * scalingFactor, np.cos(np.radians(course)) * scalingFactor, -sinkRate]
projectileLength = 17.53

minPen = 13.2
maxPen = 28.15
devPen = 5

c = 0.2
b = 0.15 / c
phi = 0.86
psi = 0.9

# 1. calculate the number of Debris
N = numberDebris(projectileMass, np.linalg.norm(projectileVelocity), 0.05)
print('N_Debris:', N)

# 2. generate debris:
# Generates an array of debris. Each row represents a piece of debris with: coordinates [0-2],
# Lc [3], A/M [4], M [5], area [6], Cw [7], and velocity magnitude in coordinate
# direction [8-10].
debris = generateDebris(projectileMass, projectileLength, projectileVelocity, pointOfImpact,
                        psi, phi, c, b, minPen, maxPen, devPen)


# improvements on generateDebris
# a. redundant columns [0-2]
# b. maybe no need for generateRandomPiece and generateMissingPiece,
#    it seems maybe a class called DebrisPiece is needed
# c. class called Debris that holds DebrisPiece
# d. the scaling of the mass couldn't have been done earlier
#    than eliminating large pieces because they would bias scaling
# e. all these scaleVelocity and enforceMomentum functions must be methods to class

