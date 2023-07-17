from .characteristicLength import *
from .areaToMass import *
from .crossSectionArea import *
from .mass import *
from .cw import *

def generateRandomPiece(pointOfImpact, projectileLength, smallestDebrisSize, numberOfParameters, c, b):
    piece = np.zeros((1, numberOfParameters))
    piece[0, :3] = pointOfImpact
    piece[0, 3] = generateCharacteristicLength(smallestDebrisSize, projectileLength)
    piece[0, 4] = areaToMassRatio(piece[0, 3])
    piece[0, 5] = surfaceAreaDebris(piece[0, 3], c, b)
    piece[0, 6] = mass(piece[0, 5], piece[0, 4], c)
    piece[0, 7] = cw()
    return piece
