import numpy as np

def generateCharacteristicLength(smallestCharacteristicLength, largestCharacteristicLength):
    # Generates the characteristic length of a debris piece. It cannot be larger than a given length,
    # and if the minimum length is undershot, it generates again.

    y = np.random.uniform(0, 1)
    L = largestCharacteristicLength * y ** 1.71
    if L >= smallestCharacteristicLength:
        characteristicLength = L
    else:
        characteristicLength = generateCharacteristicLength(smallestCharacteristicLength, largestCharacteristicLength)

    return characteristicLength