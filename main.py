from runParameter import *
from showDestinations import *

import laspy
import time

# Import Topography from file
file = laspy.read('merged2Cut.laz')
ptCloud = np.vstack((file.x, file.y, file.z)).T
pointAttributes = file.classification

# Create Dummy file with zero elevation
locationZero = np.copy(ptCloud)
locationZero[:, 2] = 0
dummyCloud = locationZero

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
runs = 1

projectileMass = 11726.27
projectileVelocity = [np.sin(np.radians(course)) * scalingFactor, np.cos(np.radians(course)) * scalingFactor, -sinkRate]
print(np.linalg.norm(projectileVelocity))
projectileLength = 17.53

minPen = 13.2
maxPen = 28.15
devPen = 5

c = 0.2
b = 0.15 / c
phi = 0.86
psi = 0.9

# Start timer
start_time = time.time()

# Run simulation
storageDestinations, debris = runParameter(runs, ptCloud, dummyCloud, lowestPoint, projectileMass, projectileLength,
                                           projectileVelocity, pointOfImpact, psi, phi, c, b, minPen, maxPen, devPen)

# Print elapsed time
print("Elapsed time:", time.time() - start_time)

# Show destinations (assuming it is a custom function)
showDestinations(storageDestinations)
