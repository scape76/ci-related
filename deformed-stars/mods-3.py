import random
from utils import validate_and_transfer
from shared import cases
import math
import copy
import time


def create_population(population_size, bounds, target_function):
    return [create_triangle(bounds, target_function) for _ in range(population_size)]


def create_triangle(bounds, target_function):
    points = [[random.uniform(bounds[0][0], bounds[0][1]), random.uniform(bounds[1][0], bounds[1][1])] for _ in
              range(3)]

    return evaluate_triangle(points, target_function)


def evaluate_triangle(points, target_function):
    central_point = [sum(p[0] for p in points) / 3, sum(p[1] for p in points) / 3]
    try:
        best_point = min(range(3), key=lambda i: target_function(points[i][0], points[i][1]))
    except OverflowError:
        print(points)

    return {"points": points, "central_point": central_point, "best_point": best_point}


def generate_shifted_population(triangles, bounds, a, target_function):
    Pz = []

    for t in triangles:
        triangle = copy.deepcopy(t)
        best_point = triangle["best_point"]

        for i, point in enumerate(triangle["points"]):
            if i == best_point:
                triangle["points"][i] = [
                    (1 + a) * triangle["points"][i][0] - a * triangle["central_point"][0],
                    (1 + a) * triangle["points"][i][1] - a * triangle["central_point"][1]]
            else:
                triangle["points"][i] = [(point[0] + a * triangle["points"][best_point][0]) / (1 + a),
                                         (point[1] + a * triangle["points"][best_point][1]) / (1 + a)]

            triangle["points"][i] = validate_and_transfer(triangle["points"][i], bounds)

        triangle = evaluate_triangle(triangle['points'], target_function)

        Pz.append(triangle)

    return Pz


def generate_rotated_population(triangles, bounds, target_function):
    Ps = []

    for t in triangles:
        triangle = copy.deepcopy(t)
        best_point = triangle["best_point"]
        beta = random.uniform(bounds[0][0], bounds[0][1])

        for i, point in enumerate(triangle["points"]):
            if i == best_point:
                continue
            else:
                point[0] = point[0] + (point[0] - triangle["points"][best_point][0]) * math.cos(beta) - (
                        point[1] - triangle["points"][best_point][1]) * math.sin(beta)
                point[1] = point[1] + (point[1] - triangle["points"][best_point][1]) * math.sin(beta) - (
                        point[1] - triangle["points"][best_point][1]) * math.cos(beta)

                triangle["points"][i] = validate_and_transfer(point, bounds)

        triangle = evaluate_triangle(triangle['points'], target_function)

        Ps.append(triangle)

    return Ps


def generate_center_rotated_population(triangles, bounds, target_function):
    Pw = []

    for t in triangles:
        triangle = copy.deepcopy(t)
        central_point = triangle["central_point"]
        best_point = triangle["best_point"]
        alpha = random.uniform(bounds[1][0], bounds[1][1])

        for i, point in enumerate(triangle["points"]):
            if i == best_point:
                continue
            else:
                point[0] = (point[0] - central_point[0]) * math.cos(alpha) - (point[1] - central_point[1]) * math.sin(
                    alpha) + central_point[0]
                point[1] = (point[0] - central_point[0]) * math.sin(alpha) - (point[1] - central_point[1]) * math.cos(
                    alpha) + central_point[1]

                triangle["points"][i] = validate_and_transfer(point, bounds)

        triangle = evaluate_triangle(triangle['points'], target_function)

        Pw.append(triangle)

    return Pw


def selection(P, Pz, Ps, Pw, target_function):
    all = P + Pz + Ps + Pw
    all.sort(key=lambda t: target_function(t["points"][t["best_point"]][0], t["points"][t["best_point"]][1]))
    P[:] = all[:len(P)]


def mods_3(stop_criteria, target_function, bounds, a):
    P = create_population(population_size, bounds, target_function)
    best_result = float('inf')
    best_triangle = None
    avg_res = float('inf')
    prev_avg_res = 0

    start_time = time.time()
    if stop_criteria == 0:
        for _ in range(epochs):
            Pz = generate_shifted_population(P, bounds, a, target_function)
            Ps = generate_rotated_population(P, bounds, target_function)
            Pw = generate_center_rotated_population(P, bounds, target_function)

            selection(P, Pz, Ps, Pw, target_function)

            current_best_result = target_function(P[0]["points"][P[0]["best_point"]][0],
                                                  P[0]["points"][P[0]["best_point"]][1])

            if current_best_result < best_result:
                best_result = current_best_result
                best_triangle = P[0]
    elif stop_criteria == 1:
        while math.fabs(get_distance(P)) > population_values_diff:
            Pz = generate_shifted_population(P, bounds, a, target_function)
            Ps = generate_rotated_population(P, bounds, target_function)
            Pw = generate_center_rotated_population(P, bounds, target_function)

            selection(P, Pz, Ps, Pw, target_function)

            current_best_result = target_function(P[0]["points"][P[0]["best_point"]][0],
                                                  P[0]["points"][P[0]["best_point"]][1])

            if current_best_result < best_result:
                best_result = current_best_result
                best_triangle = P[0]
    else:
        while math.fabs(prev_avg_res - avg_res) > population_avg_diff:
            prev_avg_res = avg_res
            Pz = generate_shifted_population(P, bounds, a, target_function)
            Ps = generate_rotated_population(P, bounds, target_function)
            Pw = generate_center_rotated_population(P, bounds, target_function)

            selection(P, Pz, Ps, Pw, target_function)

            avg_res = avg_population_res(P, target_function)

            current_best_result = target_function(P[0]["points"][P[0]["best_point"]][0],
                                                  P[0]["points"][P[0]["best_point"]][1])

            if current_best_result < best_result:
                best_result = current_best_result
                best_triangle = P[0]

    end_time = time.time()
    duration = end_time - start_time

    return best_result, best_triangle, duration


population_size = 30
compression_coefficient = 3
epochs = 1000
population_values_diff = 1e-10
population_avg_diff = 1e-10

def avg_population_res(P, target_function):
    avg_result = 0
    for t in P:
        avg_result += target_function(t['points'][t['best_point']][0], t['points'][t['best_point']][1])
    avg_result /= len(P)
    return avg_result


def get_distance(population):
    t1 = population[0]
    t2 = population[1]
    [x1, y1] = t1['points'][t1['best_point']]
    [x2, y2] = t2['points'][t2['best_point']]
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


if __name__ == '__main__':
    for case in cases:
        print(case["separator"])

        best_res, best_tr, duration = mods_3(2, case["function"], case["bounds"], compression_coefficient)

        print('duration (sec): ', duration)
        print('best ', best_res, best_tr)
        print('deviation', best_res - case['minimum'])
