import math


def sigmoid(x):
    return 1 / (1 + math.exp(-x))


def sigmoid_derivative(x):
    return x * (1 - x)


def holder(x, y):
    return -math.fabs(math.sin(x) * math.cos(y) * math.exp(math.fabs(1 - (math.sqrt(x * x + y * y) / math.pi))))


def mcCormick(x, y):
    return math.sin(x + y) + math.pow((x - y), 2) - 1.5 * x + 2.5 * y + 1


def goldsteinPrice(x, y):
    return ((1 + math.pow((x + y + 1), 2) * (19 - 14 * x + 3 * x * x - 14 * y + 6 * x * y + 3 * y * y)) *
            (30 + math.pow((2 * x - 3 * y), 2) * (18 - 32 * x + 12 * x * x + 48 * y - 36 * x * y + 27 * y * y)))


cases = [
    {
        "bounds": [[-2, 2], [-2, 2]],
        "function": goldsteinPrice,
        "separator": "---------------------------THIS IS GOLDSTEIN-PRICE----------------------",
        "minimum": 3
    },
    {
        "bounds": [[-10, 10], [-10, 10]],
        "function": holder,
        "separator": "---------------------------THIS IS HOLDER----------------------",
        "minimum": -19.2085
    },
    {
        "bounds": [[-1.5, 4], [-3, 4]],
        "function": mcCormick,
        "separator": "---------------------------THIS IS McCormick--------------------------",
        "minimum": -1.9133
    },
]
