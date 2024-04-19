import math
from numpy.random import rand


def inBounds(point, bounds):
    for i in range(len(bounds)):
        if point[i] < bounds[i, 0] or point[i] > bounds[i, 1]:
            return False
    return True


# lam - amount of initial parents
def generatePopulation(lam, bounds):
    population = []
    for i in range(lam):
        candidate = None
        while (candidate is None or not inBounds(candidate, bounds)):
            candidate = bounds[:, 0] + rand(len(bounds)) * (bounds[:, 1] - bounds[:, 0])
        population.append(candidate)
    return population
