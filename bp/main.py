from utils import generateNetwork, sigmoid, sigmoid_derivative, generate_dataset, var7_func, get_expected_values


# back propagation implementation

# see https://people.engr.tamu.edu/guni/csce421/files/AI_Russell_Norvig.pdf
# page 734
# examples - set of examples, each with input vector X and output vector Y
# network - multilayer with L layers, weights w(i,j), activation function g
def backward_propagate_error(expected, network):
    for l in reversed(range(len(network))):
        layer = network[l]
        # if it's output layer
        if l == len(network) - 1:
            for j in range(len(layer)):
                neuron = layer[j]
                neuron['delta'] = sigmoid_derivative(neuron['output']) * (neuron['output'] - expected[j])
        else:
            for j in range(len(layer)):
                error = 0.0
                for neuron in network[l + 1]:
                    error += neuron['weights'][j] * neuron['delta']
                curr_neuron = layer[j]
                curr_neuron['delta'] = sigmoid_derivative(curr_neuron['output']) * error

    return network


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


def forward_propagation(inputs, network):
    for l in range(len(network)):
        layer = network[l]
        # if it's 1st hidden layer
        if l == 0:
            for neuron in layer:
                activation = activate(neuron['weights'], inputs)
                output = sigmoid(activation)
                neuron['output'] = output
        else:
            inputs = [neuron['output'] for neuron in network[l - 1]]
            for neuron in layer:
                activation = activate(neuron['weights'], inputs)
                output = sigmoid(activation)
                neuron['output'] = output
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
    network = generateNetwork(3, 4, 2)
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
