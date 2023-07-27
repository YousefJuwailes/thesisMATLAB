from ABC_HFs import *
from runParameter import *
from scipy.io import loadmat
from HF import *

import laspy
import multiprocessing
import matplotlib.pyplot as plt
import time

finalDirectory  =  "/shome/yousef_j/thesisMATLAB/LawOfLargeNumbers"


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
N = 40    # attempts to simulate a sample from the posterior
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
        phi = 0.86
        storageDestinations = runParameter(ptCloud, lowestPoint, projectileMass, projectileLength, 
                                           projectileVelocity, pointOfImpact, psi, phi, c, b, minPen, maxPen, devPen, KDTree,)
        
        acceptSample = distance(actualDebris, storageDestinations, h, pointOfImpact)
        acceptSample = True
        if acceptSample:
            phi_result.append(phi)
            storage_destinations_result.append(storageDestinations)

    results_queue.put((phi_result, storage_destinations_result))

# Multiprocessing
manager = multiprocessing.Manager()
resultsQueue = manager.Queue()
processes = []
for i in range(numberOfCores): 
    start_index = i * simulations_per_core
    end_index = (i + 1) * simulations_per_core
    process = multiprocessing.Process(
        target=run_simulation, args=(start_index, end_index, resultsQueue)
    )
    process.start()
    processes.append(process)

# Wait for all processes to finish
for process in processes:
    process.join()

# Get the results from the queue
phi = []
storageDestinations = []
while not resultsQueue.empty():
    phi_temp, storageDestinations_temp = resultsQueue.get()
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
Plot(storageDestinations[0], pointOfImpact)

print("Number of accepted samples is", len(phi))

###### Law of Large numbers test ######
###### Law of Large numbers test ######
###### Law of Large numbers test ######
###### Law of Large numbers test ######

# def vanillaSimulation(startIdx, endIdx, results):
#     N = endIdx - startIdx  
#     avgX, avgY, avgZ, stdX, stdY, length, width, angle = [], [], [], [], [], [], [], []
#     for i in range(N):
#         storageDestinations = runParameter(ptCloud, lowestPoint, projectileMass, projectileLength, 
#                                            projectileVelocity, pointOfImpact, psi, phi, c, b, minPen, maxPen, devPen, KDTree,)
#         locAvg, locStd, lengthSim, widthSim, angleSim = summaryStatistics(storageDestinations, pointOfImpact)
#         avgX.append(locAvg[0])  
#         avgY.append(locAvg[1])  
#         avgZ.append(locAvg[2])  
#         stdX.append(locStd[0])  
#         stdY.append(locStd[1])  
#         length.append(lengthSim)
#         width.append(widthSim) 
#         angle.append(angleSim)
#     results.put((avgX, avgY, avgZ, stdX, stdY, length, width, angle))

# # Multiprocessing
# manager = multiprocessing.Manager()
# resultsQueue = manager.Queue()
# processes = []
# for i in range(numberOfCores): 
#     start_index = i * simulations_per_core
#     end_index = (i + 1) * simulations_per_core
#     process = multiprocessing.Process(
#         target=vanillaSimulation, args=(start_index, end_index, resultsQueue)
#     )
#     process.start()
#     processes.append(process)

# # Wait for all processes to finish
# for process in processes:
#     process.join()

# avgX, avgY, avgZ, stdX, stdY, length, width, angle = [], [], [], [], [], [], [], []
# while not resultsQueue.empty():
#     avgX_temp, avgY_temp, avgZ_temp, stdX_temp, stdY_temp, length_temp, width_temp, angle_temp = resultsQueue.get()
#     avgX.extend(avgX_temp)
#     avgY.extend(avgY_temp)
#     avgZ.extend(avgZ_temp)
#     stdX.extend(stdX_temp)
#     stdY.extend(stdY_temp)
#     length.extend(length_temp)
#     width.extend(width_temp)
#     angle.extend(angle_temp)


# storageDestinations = runParameter(ptCloud, lowestPoint, projectileMass, projectileLength, 
#                                            projectileVelocity, pointOfImpact, psi, phi, c, b, minPen, maxPen, devPen, KDTree,)
# locAvg, locStd, lengthSim, widthSim, angleSim = summaryStatistics(storageDestinations, pointOfImpact)

# # Plotting simulated debris
# counter = 0
# for i in range(len(storageDestinations)):
#     if storageDestinations[i, 0] < 100:
#         counter += 1
#         continue
#     else:
#         plt.scatter(storageDestinations[i, 0], storageDestinations[i, 1], color='black')
# plt.scatter(pointOfImpact[0], pointOfImpact[1], color='Yellow')
# plt.scatter(locAvg[0], locAvg[1], color='red')
# plt.savefig("TopView")

# plot posterior distribution of phi
# plt.hist(avgX)
# plt.savefig(finalDirectory + "/avgX")
# plt.clf()
# plt.close()

# plt.hist(avgY)
# plt.savefig(finalDirectory + "/avgY")
# plt.clf()
# plt.close()

# plt.hist(avgZ)
# plt.savefig(finalDirectory + "/avgZ")
# plt.clf()
# plt.close()

# plt.hist(stdX)
# plt.savefig(finalDirectory + "/stdX")
# plt.clf()
# plt.close()

# plt.hist(stdY)
# plt.savefig(finalDirectory + "/stdY")
# plt.clf()
# plt.close()

# plt.hist(length)
# plt.savefig(finalDirectory + "/length")
# plt.clf()
# plt.close()

# plt.hist(width)
# plt.savefig(finalDirectory + "/width")
# plt.clf()
# plt.close()

# plt.hist(angle)
# plt.savefig(finalDirectory + "/angle")
# plt.clf()
# plt.close()