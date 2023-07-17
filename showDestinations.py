import matplotlib.pyplot as plt
import geopandas as gpd
import numpy as np

from convertShapeFileDeg2Utm import *

def showDestinations(storageDestinations):
    # Load shapefile and convert coordinates to UTM
    S = convertShapeFileDeg2Utm(gpd.read_file('buildingsRemscheid.shp'))

    # Load A6.mat file
    data = np.load('A6.mat')

    plt.figure()
    plt.clf()

    # Show Remscheid buildings
    S.plot()

    # Show destination points
    plt.scatter(storageDestinations[:, 0], storageDestinations[:, 1], marker='o', edgecolor='#4e4eff',
                facecolor='#4e4eff', alpha=0.15)

    # Show A6 points
    plt.scatter(data[:119, 0], data[:119, 1], marker='+', color='red')

    # Set plot axis limits
    plt.axis([3.714e5, 3.7165e5, 5.6717125e6, 5.67216e6])

    # Show plot
    plt.show()