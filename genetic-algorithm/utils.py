import math
from numpy.random import randint


def panximia(population, scores):
    selected = []

    for i in range(len(population)):
        randomIdx = randint(0, len(population))
        selected.append(population[randomIdx])

    return selected


def tournament_selection(population, scores, k=3):
    selected = []
    for i in range(len(population)):
        # first random selection
        selection_ix = randint(len(population))
        for ix in randint(0, len(population), k - 1):
            # check if better (e.g. perform a tournament)
            if scores[ix] < scores[selection_ix]:
                selection_ix = ix
        selected.append(population[selection_ix])
    return selected


def outcrossing(population, scores):
    selected = []

    for i in range(round(len(population) / 2)):
        partnerIdx = randint(0, len(population) - 1)
        partner = population[partnerIdx]
        partnerScore = scores[partnerIdx]

        difference = math.inf
        otherpartnerIdx = 0

        for i in range(len(scores)):
            score = scores[i]
            diff = math.fabs(score - partnerScore)
            if (diff > difference and partnerIdx != i):
                difference = diff
                otherpartnerIdx = i

        selected.append(partner)
        selected.append(population[otherpartnerIdx])

    return selected


def inbreeding(population, scores):
    selected = []

    for i in range(round(len(population) / 2)):
        partnerIdx = randint(0, len(population) - 1)
        partner = population[partnerIdx]
        partnerScore = scores[partnerIdx]

        difference = math.inf
        otherpartnerIdx = 0

        for i in range(len(scores)):
            score = scores[i]
            diff = math.fabs(score - partnerScore)
            if (diff < difference and partnerIdx != i):
                difference = diff
                otherpartnerIdx = i

        selected.append(partner)
        selected.append(population[otherpartnerIdx])

    return selected
