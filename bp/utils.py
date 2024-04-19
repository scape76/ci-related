import math
from random import random

init = [2, 5, 4]


def generateNetwork(p, l, k):
    network = list()

    hidden_layer = [{"weights": [random() for i in range(p)]} for i in range(l)]
    network.append(hidden_layer)

    output_layer = [{"weights": [random() for i in range(l)]} for i in range(k)]
    network.append(output_layer)

    return network


def var7_func(x1, x2, x3):
    return math.cos(x1) + math.cos(x2) - math.sin(x3)


def dataset_minmax(dataset):
    stats = [[min(column), max(column)] for column in dataset]
    return stats


# first function for normalizing
def normalize_dataset(dataset, minmax):
    for row in dataset:
        for i in range(len(row)):
            row[i] = (row[i] - minmax[i][0]) / (minmax[i][1] - minmax[i][0])


def generate_args(var_function):
    args = list()
    args.append(init)

    i = 0
    while len(args) < 30:
        candidate_args = args[len(args) - 1].copy()
        candidate_args[i % 3] = candidate_args[i % 3] + (1 if i % 2 == 0 else -1)
        # sigmoid bounds
        # we could pass those depending on the activation function we use
        # if 0 < result < 1:
        args.append(candidate_args)
        i += 1

    return args


def generate_dataset(var_function):
    dataset = generate_args(var_function)

    # normalizing will be redundant
    # if you uncomment line 59
    minmax = dataset_minmax(dataset)
    normalize_dataset(dataset, minmax)

    return dataset


def get_expected_values(dataset, var_function):
    results = []
    for i in range(len(dataset)):
        res = var_function(dataset[i][0], dataset[i][1], dataset[i][2])
        results.append(res)

    average = sum(results) / len(results)

    expected = []

    for i in range(len(dataset)):
        y = list()
        y.append(results[i])
        y.append(1 if results[i] > average else 0)
        expected.append(y)

    return expected
