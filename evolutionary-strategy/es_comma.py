import utils
from numpy import argsort
from numpy.random import randn
from numpy import sqrt


def es_comma(lam, mu, bounds, fitFunction, nIter, stepSize, expected):
    best, best_eval = None, 1e+10
    AS = 0
    nChildren = int(lam / mu)
    population = utils.generatePopulation(lam, bounds)

    for epoch in range(nIter):
        scores = [fitFunction(c[0], c[1]) for c in population]
        ranks = argsort(argsort(scores))
        selected = []
        for i in range(mu):
            selected.append(ranks[i])
        children = list()

        for i in selected:
            if scores[i] < best_eval:
                best, best_eval = population[i], scores[i]
                print('%d, Best: f(%s) = %.5f' % (epoch, best, best_eval))
                speed = epoch
            for _ in range(nChildren):
                child = None
                while child is None or not utils.inBounds(child, bounds):
                    child = population[i] + randn(len(bounds)) * stepSize
                children.append(child)
        population = children
        AS = AS + (best_eval - expected) ** 2
        averageSquare = sqrt(AS / nIter)

    return best, best_eval, averageSquare, speed
