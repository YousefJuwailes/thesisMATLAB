import math

def deg2utm(Lat, Lon):
    # Argument checking
    if len(Lat) != len(Lon):
        raise ValueError("Lat and Lon vectors should have the same length")

    # Memory pre-allocation
    n1 = len(Lat)
    x = [0] * n1
    y = [0] * n1
    utmzone = ['60 X'] * n1

    # Main Loop
    for i in range(n1):
        la = Lat[i]
        lo = Lon[i]

        sa = 6378137.000000
        sb = 6356752.314245

        e2 = ((sa ** 2 - sb ** 2) ** 0.5) / sb
        e2cuadrada = e2 ** 2
        c = sa ** 2 / sb

        lat = la * (math.pi / 180)
        lon = lo * (math.pi / 180)

        Huso = int((lo / 6) + 31)
        S = (Huso * 6) - 183
        deltaS = lon - (S * (math.pi / 180))

        if la < -72:
            Letra = 'C'
        elif la < -64:
            Letra = 'D'
        elif la < -56:
            Letra = 'E'
        elif la < -48:
            Letra = 'F'
        elif la < -40:
            Letra = 'G'
        elif la < -32:
            Letra = 'H'
        elif la < -24:
            Letra = 'J'
        elif la < -16:
            Letra = 'K'
        elif la < -8:
            Letra = 'L'
        elif la < 0:
            Letra = 'M'
        elif la < 8:
            Letra = 'N'
        elif la < 16:
            Letra = 'P'
        elif la < 24:
            Letra = 'Q'
        elif la < 32:
            Letra = 'R'
        elif la < 40:
            Letra = 'S'
        elif la < 48:
            Letra = 'T'
        elif la < 56:
            Letra = 'U'
        elif la < 64:
            Letra = 'V'
        elif la < 72:
            Letra = 'W'
        else:
            Letra = 'X'

        a = math.cos(lat) * math.sin(deltaS)
        epsilon = 0.5 * math.log((1 + a) / (1 - a))
        nu = math.atan(math.tan(lat) / math.cos(deltaS)) - lat
        v = (c / ((1 + (e2cuadrada * (math.cos(lat) ** 2))) ** 0.5)) * 0.9996
        ta = (e2cuadrada / 2) * epsilon ** 2 * (math.cos(lat) ** 2)
        a1 = math.sin(2 * lat)
        a2 = a1 * (math.cos(lat) ** 2)
        j2 = lat + (a1 / 2)
        j4 = ((3 * j2) + a2) / 4
        j6 = ((5 * j4) + (a2 * (math.cos(lat) ** 2))) / 3
        alfa = (3 / 4) * e2cuadrada
        beta = (5 / 3) * alfa ** 2
        gama = (35 / 27) * alfa ** 3
        Bm = 0.9996 * c * (lat - alfa * j2 + beta * j4 - gama * j6)
        xx = epsilon * v * (1 + (ta / 3)) + 500000
        yy = nu * v * (1 + ta) + Bm

        if yy < 0:
            yy = 9999999 + yy

        x[i] = xx
        y[i] = yy
        utmzone[i] = f"{Huso:02d} {Letra}"

    return x, y, utmzone