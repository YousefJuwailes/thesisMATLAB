from runParameter import *
import matplotlib.pyplot as plt

import laspy
import time

# Import Topography from file
file = laspy.read('/shome/yousef_j/Thesis/merged2Cut.laz')
ptCloud = np.vstack((file.x, file.y, file.z)).T

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
velocity = 140
scalingFactor = (velocity**2 - sinkRate**2)**0.5

# How many times the entire simulation is run
runs = 1

projectileMass = 13000
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

KDTree = cKDTree(dummyCloud[:, :2])  # Only consider x and y coordinates

# Run simulation
storageDestinations = runParameter(runs, ptCloud, dummyCloud, lowestPoint, projectileMass, projectileLength,
                                           projectileVelocity, pointOfImpact, psi, phi, c, b, minPen, maxPen, devPen, KDTree)

# Print elapsed time
print("Elapsed time:", time.time() - start_time)

counter = 0
for i in range(len(storageDestinations)):
    if storageDestinations[i, 0] < 100:
        counter += 1
        continue
    else:
        plt.scatter(storageDestinations[i, 0], storageDestinations[i, 1], color='black')

plt.scatter(pointOfImpact[0], pointOfImpact[1], color='yellow')
plt.savefig("TopView")