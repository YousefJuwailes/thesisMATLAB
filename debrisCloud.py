import math
from debrisPieceHFs import *


class DebrisCloud:
    def __init__(self, piecesNum, simParameters):
        self.simParameters = simParameters
        self.piecesArray    = self.piecesArray(piecesNum, simParameters)

        self.mass           = sum(piece.mass for piece in self.piecesArray)
        self.massCheck()

        self.KE             = sum(0.5 * piece.mass * math.pow(piece.velocityVec, 2) for piece in self.piecesArray)
        self.momentum       = sum(piece.mass * piece.velocityVec for piece in self.piecesArray)


    def massCheck(self):
        if self.mass > self.simParameters.mass:
            tooHeavy = True
            while tooHeavy:
                m, i = np.max(Debris[:, 6]), np.argmax(Debris[:, 6])
                if m >= 0.1 * projectileMass:
                    Debris = np.delete(Debris, i, axis=0)
                    newPiece = generateRandomPiece(pointOfImpact, projectileLength, smallestDebrisSize,
                                                   numberOfParameters,
                                                   c, b)
                    Debris = np.concatenate((Debris, newPiece), axis=0)
                else:
                    tooHeavy = False

        else:
            Debris = np.delete(Debris, N, axis=0)
            missingPiece = generateMissingPiece(projectileMass - totalMass,
                                                generateCharacteristicLength(smallestDebrisSize, projectileLength),
                                                numberOfParameters)
            Debris = np.concatenate((Debris, missingPiece), axis=0)

        # Ensure no piece weighs more than 10% of the total mass



x = np.zeros((10, 2))
x[:, 0] = 1
x[:, 1] = 2

y1 = sum(piece[0] for piece in x)
y2 = sum(piece[1] for piece in x)

print(y1)
print(y2)
