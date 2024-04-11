from utils import generateNetwork, sigmoid, sigmoid_derivative


# back propagation realization

# see https://people.engr.tamu.edu/guni/csce421/files/AI_Russell_Norvig.pdf
# page 734
# examples - set of examples, each with input vector X and output vector Y
# network - multilayer with L layers, weights w(i,j), activation function g
def backpropagation(examples, network):
    for [x, y] in examples:
        for i in range(len(network[1])):
            neuron = network[1][i]
            neuron['delta'] = sigmoid_derivative(neuron['output']) * (neuron['output'] - y[i])

        for i in range(len(network[0])):
            errors = 0
            for j in range(len(network[1])):
                output_neuron = network[1][j]
                errors += output_neuron['weights'][i] * output_neuron['delta']

            neuron = network[0][i]
            neuron['delta'] = sigmoid_derivative(network[0][i]['output']) * errors
    return network


# update every weight in network
def update_weights(network, learning_factor):
    for l in range(len(network)):
        for i in range(len(network[l])):
            for j in range(len(network[l][i]['weights'])):
                network[l][i]['weights'][j] = network[l][i]['weights'][j] + network[l][i]['delta'] * learning_factor


def activate(weights, inputs):
    activation = 0
    for i in range(len(weights)):
        activation += weights[i] * inputs[i]
    return activation


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
    network = forward_propagation(inputs, network)
    outputs = []
    for i in range(len(network[1])):
        outputs.append(network[1][i]['output'])

    return outputs


if __name__ == '__main__':
    network = generateNetwork(2, 3, 2)
    res = predict([4, 2], network)
    # backpropagation(
    #     [[[4, 2], [0.5, 0.5]], [[4, 2], [0.5, 0.5]], [[4, 2], [0.5, 0.5]], [[4, 2], [0.5, 0.5]]], network)
    # update_weights(network, 0.5)
    # res = predict([4, 2], network)
    # print(res)
