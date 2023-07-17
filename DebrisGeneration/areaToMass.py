import math
import random


def sigmaL11(lambda_val):
    # SIGMAL11 helper function for areaToMassDistributionL11
    if lambda_val <= -3.5:
        sigma = 0.2
    else:
        sigma = 0.2 + 0.1333 * (lambda_val + 3.5)

    return sigma


def muL11(lambda_val):
    # MUL11 helper function for areaToMassDistributionL11
    if lambda_val <= -1.75:
        mu = -0.3
    elif lambda_val < -1.25:
        mu = -0.3 - 1.4 * (lambda_val + 1.75)
    else:
        mu = -1

    return mu

def alphaG11(lambda_val):
    # ALPHAG11 helper function for areaToMassDistributionG11
    if lambda_val <= -1.4:
        alpha = 1
    elif lambda_val < 0:
        alpha = 1 - 0.3571 * (lambda_val + 1.4)
    else:
        alpha = 0.5

    return alpha

def mu1G11(lambda_val):
    # mu1G11 helper function for areaToMassDistributionG11
    if lambda_val <= -0.5:
        mu = -0.45
    elif lambda_val < 0:
        mu = -0.45 - 0.9 * (lambda_val + 0.5)
    else:
        mu = -0.9

    return mu


def sigma2G11(lambda_val):
    # SIGMA2G11 helper function for areaToMassDistributionG11
    if lambda_val <= -1:
        sigma2 = 0.28
    elif lambda_val < 0.1:
        sigma2 = 0.28 - 0.1636 * (lambda_val + 1)
    else:
        sigma2 = 0.1

    return sigma2


def areaToMassRatioL11(lambda_val):
    # AREATOMASSDISTRIBUTIONL11 returns the area-to-mass ratio for
    # particles with a characteristic length of less than 11cm after the Nasa
    # Breakupmodel 4

    # D = normpdf(chi,muL11(lambda_val),sigmaL11(lambda_val))
    D = random.normalvariate(muL11(lambda_val), sigmaL11(lambda_val))

    return D

def areaToMassRatioG11(lambda_val):
    # AREATOMASSDISTRIBUTIONG11 returns the area-to-mass ratio for
    # particles with a characteristic length of over 11cm after the Nasa
    # Breakupmodel 4
    sigma1 = 0.55
    mu2 = -0.9

    # deciding which peak
    x = random.random()

    if x < alphaG11(lambda_val):
        D = random.normalvariate(mu1G11(lambda_val), sigma1)
    else:
        D = random.normalvariate(mu2, sigma2G11(lambda_val))

    # Falsche Implementierung wie sie auch in C++ Implementierung zu finden war
    # D = alphaG11(lambda_val)*normrnd(mu1G11(lambda_val),sigma1)+(1-alphaG11(lambda_val))*normrnd(mu2,sigma2G11(lambda_val));

    return D

def areaToMassRatio(characteristicLength):
    # returns the area-to-mass ratio after the Nasa Breakup Model 4 for upper stage fragments

    lambda_val = math.log10(characteristicLength)
    if characteristicLength > 0.11:
        D = 10 ** areaToMassRatioG11(lambda_val)
    elif characteristicLength < 0.08:
        D = 10 ** areaToMassRatioL11(lambda_val)
    else:
        x = random.random()
        if x > (characteristicLength - 0.08) / 0.03:
            D = 10 ** areaToMassRatioL11(lambda_val)
        else:
            D = 10 ** areaToMassRatioG11(lambda_val)

            # erste, vermutlich falsche Implementierung, evtentuell müsste man hier
            # nochmal ne unterscheidung machen. NASA BMC++ S.28
            # D = 10^(areaToMassRatioG11(lambda_val)*(characteristicLength-0.08)/0.03+areaToMassRatioL11(lambda_val)*(1-(characteristicLength-0.08)/0.03))

    return D



