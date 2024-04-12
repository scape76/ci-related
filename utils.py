# This is a sample Python script.
import math
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from random import random, shuffle

init_args = [
    [4, 6, 7],
    [4, 6, 8],
    [4, 6, 9],
    [5, 6, 7],
    [5, 6, 8],
    [5, 6, 9],
    [5, 7, 7],
    [5, 7, 8],
    [5, 7, 9],
    [5, 8, 7],
    [5, 8, 8],
    [6, 8, 9],
    [6, 6, 7],
    [6, 6, 8],
    [6, 6, 9],
    [6, 7, 7],
    [6, 7, 8],
    [6, 7, 9],
    [6, 8, 7],
    [6, 8, 8],
    [6, 8, 9],
    [7, 7, 7],
    [7, 7, 8],
    [7, 7, 9],
    [7, 8, 7],
    [7, 8, 8],
    [7, 8, 9],
    [8, 8, 7],
    [8, 8, 8],
    [8, 8, 9],
    # [8, 9, 7]
]

shuffle(init_args)


# each neuron will have properties like weights and value
def sigmoid(x):
    return 1 / (1 + math.exp(-x))


def sigmoid_derivative(x):
    return x * (1 - x)


def generateNetwork(p, l, k):
    network = list()

    hidden_layer = [{"weights": [random() for i in range(p)]} for i in range(l)]
    network.append(hidden_layer)

    output_layer = [{"weights": [random() for i in range(l)]} for i in range(k)]
    network.append(output_layer)

    return network


def var7_func(x1, x2, x3):
    return math.cos(x1) + math.cos(x2) - math.sin(x3)


def var1_func(x1, x2, x3):
    return x1 * x1 - x2 * x2 + x3 * x3


def dataset_minmax(dataset):
    stats = [[min(column), max(column)] for column in dataset]
    return stats


# first function for normalizing
def normalize_dataset(dataset, minmax):
    for row in dataset:
        for i in range(len(row)):
            row[i] = (row[i] - minmax[i][0]) / (minmax[i][1] - minmax[i][0])


def generate_dataset():
    minmax = dataset_minmax(init_args)
    normalize_dataset(init_args, minmax)

    results = []
    for i in range(len(init_args)):
        res = var1_func(init_args[i][0], init_args[i][1], init_args[i][2])
        results.append(res)

    average = sum(results) / len(results)

    expected = []

    for i in range(len(init_args)):
        y = list()
        y.append(results[i])
        y.append(1 if results[i] > average else 0)
        expected.append(y)

    return [init_args, expected]
