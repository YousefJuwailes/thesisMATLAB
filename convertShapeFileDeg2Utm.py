from deg2utm import *

def convertShapeFileDeg2Utm(shp):
    # Loop over each shape in the shapefile
    for i in range(len(shp)):
        # Loop over each coordinate pair in the shape
        for j in range(len(shp[i].X) - 1):
            # Convert coordinates from degrees to UTM
            x, y, _ = deg2utm(shp[i].Y[j], shp[i].X[j])
            shp[i].X[j] = x
            shp[i].Y[j] = y

    return shp