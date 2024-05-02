import random
import math
import time
from utils import validate_and_transfer
from shared import mcCormick


def create_population(population_size, bounds):
    population = []
    for _ in range(population_size):
        x = random.uniform(bounds[0][0], bounds[0][1])
        y = random.uniform(bounds[1][0], bounds[1][1])
        population.append([x, y])
    return population


def parallel_transfer(point, a, alpha, bounds):
    point[0] += a * math.cos(alpha)
    point[1] += a * math.sin(alpha)
    point = validate_and_transfer(point, bounds)
    return point


def generate_parallel_transfer_population(P, bounds):
    Pz = []
    for _ in range(len(P)):
        i, j = random.sample(range(len(P)), 2)
        a = random.uniform(bounds[0][0], bounds[1][1])

        # from 0 to 360
        alpha = random.uniform(0, 2 * math.pi)

        p1 = parallel_transfer(P[i][:], a, alpha, bounds)
        p2 = parallel_transfer(P[j][:], a, alpha, bounds)

        Pz.append(p1)
        Pz.append(p2)

    return Pz


def generate_rotation_population(P, bounds):
    Ps = []
    for _ in range(len(P)):
        i, j = random.sample(range(len(P)), 2)
        beta = random.uniform(0, 2 * math.pi)

        p1 = P[i][:]
        p2 = P[j][:]

        x_diff = p2[0] - p1[0]
        y_diff = p2[1] - p1[1]

        # rotation relative to the p1's x and y
        p2x = p2[0] + x_diff * math.cos(beta) - y_diff * math.sin(beta)
        p2y = p2[1] + x_diff * math.sin(beta) + y_diff * math.cos(beta)

        p2 = [p2x, p2y]
        p1 = validate_and_transfer(p1, bounds)
        p2 = validate_and_transfer(p2, bounds)

        Ps.append(p1)
        Ps.append(p2)

    return Ps


def generate_compression_population(P, target_function, compression_coefficient):
    Pw = []
    for _ in range(len(P)):
        i, j = random.sample(range(len(P)), 2)

        p1 = P[i][:]
        p2 = P[j][:]

        p1_score = target_function(p1[0], p1[1])
        p2_score = target_function(p2[0], p2[1])

        # compress to the direction of better point
        if p1_score < p2_score:
            p1[0] = (p1[0] + p2[0]) / compression_coefficient
            p1[1] = (p1[1] + p2[1]) / compression_coefficient
        else:
            p2[0] = (p2[0] + p1[0]) / compression_coefficient
            p2[1] = (p2[1] + p1[1]) / compression_coefficient

        Pw.append(p1)
        Pw.append(p2)

    return Pw


def selection(P, Pz, Ps, Pw, target_function):
    combined_population = P + Pz + Ps + Pw
    combined_population.sort(key=lambda x: target_function(x[0], x[1]))
    P[:] = combined_population[:len(P)]


def deformed_stars(population_size, compression_coefficient, epochs, bounds, target_function):
    P = create_population(population_size, bounds)
    best_result = 0

    start_time = time.time()

    for _ in range(epochs):
        Pz = generate_parallel_transfer_population(P, bounds)
        Ps = generate_rotation_population(P, bounds)
        Pw = generate_compression_population(P, target_function, compression_coefficient)
        selection(P, Pz, Ps, Pw, target_function)
        best_result = target_function(P[0][0], P[0][1])

    end_time = time.time()

    duration = end_time - start_time

    return duration, best_result


duration, best_result = deformed_stars(20, 2, 1000, [[-1.5, 4], [-3, 4]], mcCormick)

print('duration (sec) ', duration, ' best_result ', best_result)
