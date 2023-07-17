from .cw import *
from .crossSectionArea import *

def generateMissingPiece(missingMass, characteristicLength, numberOfParameters):
    piece = np.zeros((1, numberOfParameters))

    # Characteristic length
    piece[0, 3] = characteristicLength

    # Surface Area
    piece[0, 5] = surfaceAreaDebris(piece[0, 3], c, b)

    # Mass
    piece[0, 6] = missingMass

    # Area-to-Mass Ratio
    piece[0, 4] = piece[0, 5] / piece[0, 6]

    # CW value
    piece[0, 7] = cw()

    return piece
