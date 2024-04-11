# This is a sample Python script.
import math
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from random import random


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
