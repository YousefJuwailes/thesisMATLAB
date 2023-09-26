from ABC_HFs        import *
from runParameter   import *
from scipy.io       import loadmat
from HF             import *

import time

finalDirectory  =  "/shome/yousef_j/thesisMATLAB/LawOfLargeNumbers"

file = laspy.read('/shome/yousef_j/ThesisSept/Metadata/merged2Cut.laz')
ptCloud = np.vstack((file.x, file.y, file.z)).T

# import relevant data
data = loadmat('A6.mat')
actualDebris    = data['A']
actualDebris    = actualDebris[:119]

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
t0 = time.time()
for i in range(1):
    storageDestinations = runParameter(ptCloud, 190, projectileMass, 
                                       projectileLength, projectileVelocity, pointOfImpact, 
                                       psi, phi, c, b, minPen, maxPen, devPen)
    
tf = time.time()
print(tf-t0)