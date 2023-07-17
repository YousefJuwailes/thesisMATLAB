def mass(surfaceArea, areaToMassRatio, c):
    # Returns the mass based on the surface area, area-to-mass ratio, and a constant.

    M = surfaceArea / (areaToMassRatio * c)
    return M