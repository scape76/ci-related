from utils import generateNetwork, sigmoid, sigmoid_derivative, generate_dataset, var7_func, get_expected_values


# back propagation realization

# see https://people.engr.tamu.edu/guni/csce421/files/AI_Russell_Norvig.pdf
# page 734
# examples - set of examples, each with input vector X and output vector Y
# network - multilayer with L layers, weights w(i,j), activation function g
def backward_propagate_error(expected, network):
    for i in range(len(network[1])):
        neuron = network[1][i]
        neuron['delta'] = sigmoid_derivative(neuron['output']) * (neuron['output'] - expected[i])

    for i in range(len(network[0])):
        errors = 0
        for j in range(len(network[1])):
            output_neuron = network[1][j]
            errors += output_neuron['weights'][i] * output_neuron['delta']

        neuron = network[0][i]
        neuron['delta'] = sigmoid_derivative(neuron['output']) * errors

    return network


# def backward_propagate_error(network, expected):
#     for i in reversed(range(len(network))):
#         layer = network[i]
#         errors = list()
#         if i != len(network) - 1:
#             for j in range(len(layer)):
#                 error = 0.0
#                 for neuron in network[i + 1]:
#                     error += (neuron['weights'][j] * neuron['delta'])
#                 errors.append(error)
#         else:
#             for j in range(len(layer)):
#                 neuron = layer[j]
#                 errors.append(neuron['output'] - expected[j])
#         for j in range(len(layer)):
#             neuron = layer[j]
#             neuron['delta'] = errors[j] * sigmoid_derivative(neuron['output'])


# update every weight in network
def update_weights(network, inputs, learning_rate):
    for l in range(len(network)):
        if l != 0:
            inputs = [neuron['output'] for neuron in network[l - 1]]
        for neuron in network[l]:
            for i in range(len(inputs)):
                neuron['weights'][i] -= neuron['delta'] * inputs[i] * learning_rate


def activate(weights, inputs):
    activation = 0
    for i in range(len(weights)):
        activation += weights[i] * inputs[i]
    return activation


# this function currently works on an assumption
# that we have only 1 hidden layer
# it's better to generalize algorithm, so it would work
# regardless of the layers amount
def forward_propagation(inputs, network):
    hidden_values = list()
    # go through inputs and get values for hidden layer
    for i in range(len(network[0])):
        activation = activate(network[0][i]['weights'], inputs)
        value = sigmoid(activation)
        network[0][i]['output'] = value
        hidden_values.append(value)
    # go through hidden layer and get values for outputs
    for i in range(len(network[1])):
        activation = activate(network[1][i]['weights'], hidden_values)
        network[1][i]['output'] = sigmoid(activation)

    return network


def predict(inputs, network):
    forward_propagation(inputs, network)
    outputs = []
    for i in range(len(network[1])):
        outputs.append(network[1][i]['output'])

    return outputs


epochs = 10000

training_amount = 24
test_amount = 30 - training_amount
learning_rate = 0.1

my_variant_function = var7_func

if __name__ == '__main__':
    network = generateNetwork(3, 3, 2)
    dataset = generate_dataset(var7_func)
    expected = get_expected_values(dataset, my_variant_function)

    training_dataset = dataset[0:training_amount]

    for _ in range(epochs):
        for i in range(training_amount):
            # expected results
            Y = expected[i]
            # input values
            X = training_dataset[i]
            forward_propagation(X, network)
            backward_propagate_error(Y, network)
            update_weights(network, X, learning_rate)

    testing_dataset = dataset[training_amount:]

    for i in range(test_amount):
        print('-----------------------------')
        print('inputs: ', testing_dataset[i])
        res = predict(testing_dataset[i], network)
        Y = expected[training_amount + i]
        print('result: ', res)
        print('expected: ', Y)
