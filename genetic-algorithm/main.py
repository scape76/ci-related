from numpy.random import randint
from utils import inbreeding, tournament_selection, panximia, outcrossing
from random import random
from math import fabs
from shared import goldsteinPrice, mcCormick, holder


def decode(bounds, number_of_bits, bitstring):
    # list of arguments x and y
    decoded = list()
    # largest possible value
    largest = 2 ** number_of_bits

    # for each argument in bounds (x and y) in our case
    for i in range(len(bounds)):
        # start and the end of bitstring that represents an argument
        # for x - from 0 to number_of_bits (16), for y - 16 to 32
        start, end = i * number_of_bits, (i * number_of_bits) + number_of_bits
        substring = bitstring[start:end]
        # convert array of bits to string of bits
        chars = ''.join([str(s) for s in substring])
        integer = int(chars, 2)
        # scale converted integer to our range (represented by bounds)
        value = bounds[i][0] + (integer / largest) * (bounds[i][1] - bounds[i][0])
        decoded.append(value)
    return decoded


def generate_population(size, bounds, number_of_bits):
    # an individual is just a string
    # which accurately represent itself
    # in our case, our individual will represent
    # a pair of x and y (arguments of a function)
    # each of them, is just a decimal value,
    # so we will construct our string to look sum like that:
    # 010011001101101 where the first half of the string
    # is the x argument, and the second is the y argument
    return [randint(0, 2, number_of_bits * len(bounds)).tolist() for _ in range(size)]


def crossover(p1, p2, cross_rate):
    c1, c2 = p1.copy(), p2.copy()

    if random() < cross_rate:
        # crossover point on a chromosome
        point = randint(0, len(p1) - 2)
        c1 = p1[:point] + p2[point:]
        c2 = p2[:point] + p1[point:]

    return [c1, c2]


def mutation(individual, mutation_rate):
    if random() < mutation_rate:
        point = randint(0, len(individual))
        individual[point] = 1 - individual[point]

    return individual


# see https://people.engr.tamu.edu/guni/csce421/files/AI_Russell_Norvig.pdf
# page 129
def genetic_algorithm(population_size, number_of_bits, fitness_function, bounds, selection_function, epochs):
    population = generate_population(population_size, bounds, number_of_bits)
    decoded_chromosome = decode(bounds, number_of_bits, population[0])

    best_individual = decoded_chromosome
    best_score = fitness_function(best_individual[0], best_individual[1])

    for generation in range(epochs):
        decoded = [decode(bounds, number_of_bits, individual) for individual in population]
        scores = [fitness_function(decoded_individual[0], decoded_individual[1]) for decoded_individual in decoded]

        # get current best score
        for i in range(population_size):
            if scores[i] < best_score:
                best_individual = decoded[i]
                best_score = scores[i]

                print('generation #', generation, ' best score:', best_score)

        # selection process
        selected = selection_function(population, scores)

        children = list()

        for i in range(0, population_size, 2):
            p1, p2 = selected[i], selected[i + 1]
            for child in crossover(p1, p2, cross_rate):
                mutation(child, mutation_rate)

                children.append(child)

        population = children

    return best_individual, best_score


epochs = 1000
population_size = 100
cross_rate = 0.9
mutation_rate = 0.7
number_of_bits = 16

fitness_functions = [{
    'name': 'Mc Cormick',
    'function': mcCormick,
    'bounds': [[-1.5, 4], [-3, 4]],
    'expected': -1.9133
},
    {
        'name': 'Goldstein Price',
        'function': goldsteinPrice,
        'bounds': [[-2, 2], [-2, 2]],
        'expected': 3
    },
    {
        'name': 'Holder',
        'function': holder,
        'bounds': [[-10, 10], [-10, 10]],
        'expected': -19.2085
    }
]

selection_functions = [{'name': 'inbreeding', 'function': inbreeding},
                       {'name': 'tournament_selection', 'function': tournament_selection},
                       {'name': 'panximia', 'function': panximia}, {'name': 'outcrossing', 'function': outcrossing}]

# if __name__ == '__main__':
#     for f_item in fitness_functions:
#         for s_item in selection_functions:
#             print('-----------------------------', s_item['name'], f_item['name'], '-----------------------------')
#             best_individual, best_score = genetic_algorithm(population_size, number_of_bits, f_item['function'],
#                                                             f_item['bounds'],
#                                                             s_item['function'], epochs)
#             error = fabs(best_score - f_item['expected'])
#             print('best ', best_individual, best_score)
#             print('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
#             print('error', error)
#             print('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
#
#         averaged_error = error / len(selection_functions)

if __name__ == '__main__':
    for f_item in fitness_functions:
        print('-----------------------------', selection_functions[1]['name'], f_item['name'],
              '-----------------------------')
        best_individual, best_score = genetic_algorithm(population_size, number_of_bits, f_item['function'],
                                                        f_item['bounds'],
                                                        selection_functions[1]['function'], epochs)
        error = fabs(best_score - f_item['expected'])
        print('best ', best_individual, best_score)
        print('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
        print('error', error)
        print('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')

    averaged_error = error / len(selection_functions)
