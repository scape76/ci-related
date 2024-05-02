import numpy as np
import math

means = [0.6926283485363582, 0.903776922809556, 7.791696452023861, 5.312331027797374, 0.8959532021754602,
         1.5547227718655, 0.6032034719546031, 6.613343432068357, 2.546878801117952]
sigmas = [2.88215010756516, 3.1559766501624207, 9.799563183713435, 0.1720626857534724, 2.2251951987724263,
          7.047313705236673, 9.647698658407682, 3.9495180904460767, 2.5936910659289527]


def normalize_data(input_data):
    normalized_data = input_data.copy()
    for j in range(input_data.shape[1]):
        max_val = np.max(input_data[:, j])
        min_val = np.min(input_data[:, j])
        normalized_data[:, j] = (input_data[:, j] - min_val) / (max_val - min_val) if max_val != min_val else 0
    return normalized_data


def forward_propagate(row, first_layer, fourth_layer):
    for i in range(0, rules_amount):
        first_layer[i]['x'] = row[0]

    for i in range(rules_amount, rules_amount * 2):
        first_layer[i]['x'] = row[1]

    for i in range(rules_amount * 2, len(first_layer)):
        first_layer[i]['x'] = row[2]

    weights = [0] * rules_amount

    for i in range(rules_amount):
        for j in range(i, len(first_layer), rules_amount):
            neuron = first_layer[j]
            weights[i] += math.exp(-math.pow((neuron['x'] - neuron['mean']) / neuron['sigma'], 2))

    weights_sum = sum(weights)
    weights = [weight / weights_sum for weight in weights]

    q_values = [0] * rules_amount
    for i in range(rules_amount):
        neuron = fourth_layer[i]
        neuron['values'] = row[:3]
        neuron['w'] = weights[i]
        q_values[i] = neuron['w'] * sum(
            value * constant for value, constant in zip(neuron['values'], neuron['weights']))

    return sum(q_values)


def start_training(data, epochs, first_layer, fourth_layer):
    for epoch in range(epochs):
        epoch_error = 0.0

        for row in data:
            result = forward_propagate(row, first_layer, fourth_layer)
            error = result - row[3]
            update_weights(error, first_layer, fourth_layer)
            epoch_error += error
        epoch_error = epoch_error / 24

        print("#", epoch + 1, " Похибка ", epoch_error)
        if (epoch_error < eps):
            break


def update_weights(error, first_layer, fourth_layer):
    denominator = sum(
        math.exp(-math.pow((neuron['x'] - neuron['mean']) / neuron['sigma'], 2)) for neuron in first_layer)

    for i in range(len(fourth_layer)):
        numerator = 1
        for j in range(i, len(first_layer), rules_amount):
            neuron = first_layer[j]
            numerator *= math.exp(-math.pow((neuron['x'] - neuron['mean']) / neuron['sigma'], 2))

        for i in range(len(fourth_layer[i]['weights'])):
            fourth_layer[i]['weights'][i] = fourth_layer[i]['weights'][i] - learning_rate * error * \
                                            fourth_layer[i]['values'][i] * numerator / denominator


def generate_network(data, means, sigma):
    first_layer = [{"x": 0, "mean": 0, "sigma": 0} for _ in range((len(data[0]) - 1) * rules_amount)]

    fourth_layer = [{"w": 0, "weights": [np.random.random() for _ in range(len(data[0]) - 1)], "values": []} for _ in
                    range(rules_amount)]

    for i, neuron in enumerate(first_layer):
        neuron["mean"] = means[i]
        neuron["sigma"] = sigma[i]

    return first_layer, fourth_layer


data = np.array([
    [1, 32, 3, 3.141362],
    [2, 32, 2, 6.29715],
    [3, 45, 3, 0.316198],
    [4, 65, 4, 2.229754],
    [5, 3, 53, 12.56472],
    [6, 2, 23, 0.973952],
    [7, 1, 12, 1.339259],
    [8, 5, 6, 46.39461],
    [9, 4, 5, 1.551375],
    [5, 3, 7, 12.8396],
    [4, 7, 6, 1.986992],
    [3, 5, 4, 0.673534],
    [2, 2, 11, 5.947558],
    [1, 8, 21, 3.146682],
    [2, 2, 21, 5.64757],
    [6, 11, 76, 0.405182],
    [7, 24, 34, 1.219278],
    [8, 56, 54, 47.27631],
    [9, 75, 23, 1.770304],
    [23, 43, 76, 3.150859],
    [43, 32, 32, 3.245165],
    [23, 21, 16, 2.905126],
    [54, 43, 38, 0.849992],
    [34, 21, 43, 1.380608],
    [12, 21, 34, 0],
    [14, 14, 14, 0],
    [20, 20, 20, 0],
])

normalized = normalize_data(data)

training_data = normalized[:-3]
testing_data = normalized[-3:]

epochs_number = 1000
learning_rate = 0.2
eps = 0.001
rules_amount = 3

l1, l4 = generate_network(data, means, sigmas)
start_training(training_data, epochs_number, l1, l4)

print("=============== predicting ===============")

for row in testing_data:
    result = forward_propagate(row, l1, l4)
    print("row ", row[:3], " result -> ", result)
