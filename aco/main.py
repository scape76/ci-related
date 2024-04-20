from random import randint, random, randrange, uniform
from math import inf
from utils import distances, idx_to_name
import numpy as np

alpha = 1.0
beta = 2.0

p = 0.9

nodes_count = len(distances)

pheromones = np.ones(distances.shape) / len(distances)

n_best = 1


def aco_algorithm(iterations):
    global pheromones
    best_path = ("", np.inf)

    for i in range(iterations):
        all_paths = generate_all_paths()
        spread_pheromone(all_paths, n_best)
        shortest_path = min(all_paths, key=lambda x: x[1])
        if shortest_path[1] <= best_path[1]:
            best_path = shortest_path
        pheromones = pheromones * p
    return best_path


def spread_pheromone(all_paths, n_best):
    sorted_paths = sorted(all_paths, key=lambda x: x[1])
    for path, dist in sorted_paths[:n_best]:
        for move in path:
            pheromones[move] += 1.0 / distances[move]


def gen_path_dist(path):
    total_dist = 0
    for ele in path:
        total_dist += distances[ele]
    return total_dist


def generate_all_paths():
    all_paths = []
    for i in range(20):
        path = generate_path(0)
        all_paths.append((path, gen_path_dist(path)))
    return all_paths


def pick_move(pheromone, distance, visited):
    pheromone = np.copy(pheromone)
    pheromone[list(visited)] = 0

    row = pheromone ** alpha * ((1.0 / distance) ** beta)

    normalized_row = row / row.sum()
    move = np.random.choice(range(nodes_count), 1, p=normalized_row)[0]

    return move


def generate_path(start):
    path = []
    visited = set()
    visited.add(start)
    prev = start
    for i in range(nodes_count - 1):
        move = pick_move(pheromones[prev], distances[prev], visited)
        path.append((prev, move))
        prev = move
        visited.add(move)
    path.append((prev, start))
    return path


def printRoute(path):
    for [from_i, to_i] in path:
        print(idx_to_name[from_i], " -> ")
    print(idx_to_name[path[0][0]])


def reshuffle_map(arr, target):
    new_arr = []
    idx = 0
    for i in range(len(arr)):
        if arr[i][1] == target:
            idx = i

    for i in range(idx + 1, len(distances)):
        new_arr.append(arr[i])

    for i in range(0, idx + 1):
        new_arr.append(arr[i])

    return new_arr


if __name__ == '__main__':
    [best_path, best_length] = aco_algorithm(100)
    res = reshuffle_map(best_path, 6)
    print('best path: ', res)
    print('best length: ', best_length)
    printRoute(res)
