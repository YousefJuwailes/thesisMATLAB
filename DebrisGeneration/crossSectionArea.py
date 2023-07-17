def surfaceAreaDebris(characteristicLength, c, b):
    if characteristicLength < 0.00167:
        A = 0.540424 * characteristicLength ** 2
    elif characteristicLength <= 4.6:
        A = 0.556945 * characteristicLength ** 2.0047077
    else:
        A = 0.556945 * 4.6 ** 2.0047077 + b * (characteristicLength - 4.6)
        A = c * A

    return A