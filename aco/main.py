from random import randint, random

K = 20
v = 0.2


def generate_ant_population(amount):
    return ["ant" for _ in range(amount)]


def generate_paths(amount):
    return [{"length": randint(1, 10), "pheromone_level": 1} for _ in range(amount)]


def update_pheromone(path):
    path["pheromone_level"] += K / path["length"]


def evaporate(path):
    path["pheromone_level"] *= v


# r - level of pheromone on one path
# sum - sum of all levels
def calculate_probability(r, sum):
    return r / sum


epochs = 2000

if __name__ == '__main__':
    paths = generate_paths(2)
    ants = generate_ant_population(10)

    print("paths before:", paths)

    for i in range(epochs):
        for ant in ants:
            pheromone_sum = 0
            for path in paths:
                pheromone_sum += path['pheromone_level']

            c1 = calculate_probability(paths[0]['pheromone_level'], pheromone_sum)

            if (c1 < random()):
                update_pheromone(paths[0])
            else:
                update_pheromone(paths[1])

            c2 = calculate_probability(paths[0]['pheromone_level'], pheromone_sum)

            if (c2 < random()):
                update_pheromone(paths[0])
            else:
                update_pheromone(paths[1])

            for path in paths:
                evaporate(path)

    print("paths after:", paths)
