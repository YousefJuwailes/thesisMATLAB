import matplotlib.pyplot as plt
import numpy as np
import sys

def Plot(data, pointOfImpact):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_xlim([371460, 371560])
    ax.set_ylim([5671800, 5672150])
    for i in range(len(data)):
        if np.all(data[i, :3] == 0):
            pass
        else:
            ax.scatter(data[i, 0], data[i, 1], color='black')
    ax.scatter(pointOfImpact[0], pointOfImpact[1], color='red')
    filename = "figureTopView.png"
    plt.savefig(filename)

    # spectator's 3D view
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    counter = 0
    for i in range(len(data)):
        if np.all(data[i, 0] == 0):
            counter += 1
        else:
            ax.scatter(data[i, 0], data[i, 1], data[i, 2], s=4, alpha=0.5, color='black')
    ax.scatter(pointOfImpact[0], pointOfImpact[1], pointOfImpact[2], color='red')
    ax.xaxis.set_major_locator(plt.MaxNLocator(3))
    ax.yaxis.set_major_locator(plt.MaxNLocator(3))
    plt.savefig("figure.png")

    # Set the viewing angle
    angle = 0
    ax.view_init(elev=0, azim=angle)
    ax.xaxis.set_major_locator(plt.MaxNLocator(3))
    ax.yaxis.set_major_locator(plt.MaxNLocator(3))
    filename = "figureSideView{}.png".format(angle)
    plt.savefig(filename)

    angle = 90
    ax.view_init(elev=0, azim=angle)
    ax.xaxis.set_major_locator(plt.MaxNLocator(3))
    ax.yaxis.set_major_locator(plt.MaxNLocator(3))
    filename = "figureSideView{}.png".format(angle)
    plt.savefig(filename)

    angle = 180
    ax.view_init(elev=0, azim=angle)
    ax.xaxis.set_major_locator(plt.MaxNLocator(3))
    ax.yaxis.set_major_locator(plt.MaxNLocator(3))
    filename = "figureSideView{}.png".format(angle)
    plt.savefig(filename)

    angle = 270
    ax.view_init(elev=0, azim=angle)
    ax.xaxis.set_major_locator(plt.MaxNLocator(3))
    ax.yaxis.set_major_locator(plt.MaxNLocator(3))
    filename = "figureSideView{}.png".format(angle)
    plt.savefig(filename)