import numpy as np

def summaryStatistics(debrisLocations, pointOfImpact):
    # summary statistics for the data
    #1. average location and its std
    debrisLocations = debrisLocations[debrisLocations[:, 0] >= 100]
    locAvg = np.array([
        np.average(debrisLocations[:, 0]),
        np.average(debrisLocations[:, 1])
    ])
    locStd = np.array([
        np.std(debrisLocations[:, 0]),
        np.std(debrisLocations[:, 1])
    ])

    #2. area covered by the debris
    excludedIndicies = []
    for i in range(len(debrisLocations)):
        if abs(debrisLocations[i, 0] - pointOfImpact[0]) > abs(locAvg[0] - pointOfImpact[0]) + 3*locStd[0]:
            excludedIndicies.append(i)
            continue
        elif abs(debrisLocations[i, 1] - pointOfImpact[1]) > abs(locAvg[1] - pointOfImpact[1]) + 3*locStd[0]:
            excludedIndicies.append(i)
            continue

    Xmax, Xmin = np.max(np.delete(debrisLocations[:, 0], excludedIndicies)), np.min(np.delete(debrisLocations[:, 0], excludedIndicies))
    Ymax, Ymin = np.max(np.delete(debrisLocations[:, 1], excludedIndicies)), np.min(np.delete(debrisLocations[:, 1], excludedIndicies))
    length  = Xmax - Xmin
    width   = Ymax - Ymin

    #3. angle the avg point makes wrt crash location
    vec     = locAvg[:2] - pointOfImpact[:2]
    angle   = np.rad2deg(np.arctan(vec[1]/vec[0]))
    
    return locAvg, locStd, length, width, angle


def distance(actualDebris, simulatedDebris, e, pointOfImpact):
    mask = np.all(simulatedDebris == 0, axis=1)
    simulatedDebris = simulatedDebris[~mask]
    sim_locAvg, sim_locStd, sim_length, sim_width, sim_angle = summaryStatistics(simulatedDebris, pointOfImpact)

    # tolerance check
    counter = 0
    locAvg, locStd, length, width, angle = summaryStatistics(actualDebris, pointOfImpact)
    if (1-e)*locAvg[0] <= sim_locAvg[0] <= locAvg[0]*(1+e):
        counter += 1
    if (1-e)*locAvg[1] <= sim_locAvg[1] <= locAvg[1]*(1+e):
        counter += 1
    # if (1-e)*locStd[0] <= sim_locStd[0] <= locStd[0]*(1+e):
    #     counter += 1
    # if (1-e)*locStd[1] <= sim_locStd[1] <= locStd[1]*(1+e):
    #     counter += 1
    if (1-e)*length <= sim_length <= length*(1+e):
        counter += 1
    if (1-e)*width <= sim_width <= width*(1+e):
        counter += 1
    if abs((1-e)*angle) <= abs(sim_angle) <= abs(angle*(1+e)):
        counter += 1

    # print(counter)
    if counter >= 5:
        return True
    else:
        return False