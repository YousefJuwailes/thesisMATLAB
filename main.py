from ABC_HFs import *
from runParameter import *

import laspy
import multiprocessing
import matplotlib.pyplot as plt
import time

from scipy.io import loadmat

# import relevant data
data = loadmat('A6.mat')
actualDebris    = data['A']
actualDebris    = actualDebris[:119]

file = laspy.read('/shome/yousef_j/Thesis/merged2Cut.laz')
ptCloud = np.vstack((file.x, file.y, file.z)).T
KDTree = cKDTree(ptCloud[:, :2])
lowestPoint = 190

# Course after bouncing off the house
course = 167.54

# Inverted Sink Rate
sinkRate = -58
velocity = 140
scalingFactor = (velocity**2 - sinkRate**2)**0.5

projectileMass = 13000
projectileVelocity = [np.sin(np.radians(course)) * scalingFactor, np.cos(np.radians(course)) * scalingFactor, -sinkRate]
projectileLength = 17.53
pointOfImpact = [371468.11, 5672127.86, 290]

minPen = 13.2
maxPen = 28.15
devPen = 5

c = 0.2
b = 0.15 / c

phi = 0.86
psi = 0.9

# Start timer
start_time = time.time()

# ABC and multiprocessing parameters
h = 0.2     # tolerence is 10%
N = 1000    # attempts to simulate a sample from the posterior
numberOfCores = 40
simulations_per_core = int(N/numberOfCores)

# Function to run the simulation for a given index range
def run_simulation(start_index, end_index, results_queue):
    # Number of attempts to simulate a sample from the posterior
    N = end_index - start_index  
    
    phi_result = []
    storage_destinations_result = []
    for i in range(N):
        phi = np.random.uniform(0.81, 0.95)
        storageDestinations = runParameter(ptCloud, lowestPoint, projectileMass, projectileLength, 
                                           projectileVelocity, pointOfImpact, psi, phi, c, b, minPen, maxPen, devPen, KDTree,)
        
        acceptSample = distance(actualDebris, storageDestinations, h, pointOfImpact)
        if acceptSample:
            phi_result.append(phi)
            storage_destinations_result.append(storageDestinations)

    results_queue.put((phi_result, storage_destinations_result))

# Multiprocessing
manager = multiprocessing.Manager()
results_queue = manager.Queue()
processes = []
for i in range(numberOfCores): 
    start_index = i * simulations_per_core
    end_index = (i + 1) * simulations_per_core
    process = multiprocessing.Process(
        target=run_simulation, args=(start_index, end_index, results_queue)
    )
    process.start()
    processes.append(process)

# Wait for all processes to finish
for process in processes:
    process.join()

# Get the results from the queue
phi = []
storageDestinations = []
while not results_queue.empty():
    phi_temp, storageDestinations_temp = results_queue.get()
    phi.extend(phi_temp)
    storageDestinations.extend(storageDestinations_temp)

# Print elapsed time
print("Elapsed time:", time.time() - start_time)

# plot posterior distribution of phi
plt.hist(phi)
plt.savefig("phiPosterior_N1000")
plt.clf()
plt.close()

# Plotting simulated debris
counter = 0
for i in range(len(storageDestinations[0])):
    if storageDestinations[0][i, 0] < 100:
        counter += 1
        continue
    else:
        plt.scatter(storageDestinations[0][i, 0], storageDestinations[0][i, 1], color='black')
plt.scatter(pointOfImpact[0], pointOfImpact[1], color='yellow')
plt.savefig("TopView")

print("Number of accepted samples is", len(phi))