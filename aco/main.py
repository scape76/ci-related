from random import randint, random, randrange, uniform
from math import inf
from utils import distances

K = 20
h = 2

nodes_count = len(distances)

pheromones = [[1 for _ in range(nodes_count)] for _ in range(nodes_count)]

best_length = +inf


def calculate_probability(idx1, idx2):
    s = sum(pow((elem + K), h) for elem in pheromones[idx1])
    return (pow(pheromones[idx1][idx2] + K, h)) / s


# def calculate_probability(idx1, idx2):
#    return pow(pheromones[idx1][idx2], alpha) * pow(pheromones[idx1][idx2], -beta)


def aco_algorithm(batch_size):
    global best_length

    for i in range(nodes_count):
        for j in range(nodes_count):
            pheromones[i][j] *= 0.999

    new_pheromones = pheromones.copy()

    for _i in range(batch_size):
        [path, distance] = get_random_path_from(17)
        if distance < best_length:
            best_length = distance
        difference = distance - best_length + 0.01  # to not divide by zero
        w = 0.01 / difference
        for i in range(nodes_count + 1):
            idx1 = path[i % nodes_count]
            idx2 = path[(i + 1) % nodes_count]
            new_pheromones[idx1][idx2] += w
            new_pheromones[idx2][idx1] += w

    for i in range(nodes_count):
        n_sum = 0.0
        for j in range(nodes_count):
            if i == j:
                continue
            n_sum += new_pheromones[i][j]
        for j in range(nodes_count):
            pheromones[i][j] = 2 * new_pheromones[i][j] / n_sum

    return best_length


def get_random_path_from(indx):
    path = []
    dist = 0
    path.append(indx)
    current_indx = indx
    while (len(path) < nodes_count):
        n_sum = 0.0
        possible_next = []
        for n in range(nodes_count):
            if (n in path):
                continue
            n_sum += calculate_probability(current_indx, n)
            possible_next.append(n)
        r = uniform(0.0, n_sum)
        x = 0.0
        for nn in possible_next:
            x += calculate_probability(current_indx, nn)
            if r <= x:
                dist += distances[current_indx][nn]
                current_indx = nn
                path.append(nn)
                break
    dist += distances[current_indx][indx]
    return [path, dist]


if __name__ == '__main__':
    best_path = aco_algorithm(2000)
    print('best path: ', best_path)
    print(pheromones)
    # [path, dist] = get_random_path_from(7)
    # total_distance = sum(distances[path[i]][path[i + 1]] for i in range(len(path) - 1))
    # print(total_distance + distances[path[len(path) - 1]][7])
