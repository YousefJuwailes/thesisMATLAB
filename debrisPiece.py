from debrisPieceHFs import *


class DebrisPiece:
    def __init__(self, c, b, LcMax, LcMin):
        self.Lc                         = generateCharacteristicLength(LcMin, LcMax)
        self.AMratio                    = areaToMassRatio(self.Lc )
        self.Ax                         = surfaceAreaDebris(self.Lc, c, b)
        self.mass                       = mass(self.Ax, self.AMratio, c)
        self.dragCoef                   = cw()

        self.velocityVec                = None
        self.penetration_distance       = None