def validate_and_transfer(point, bounds):
    x_bounds, y_bounds = bounds

    if point[0] < x_bounds[0] and point[1] < y_bounds[0]:
        point[0] -= (x_bounds[0] - x_bounds[1])
        point[1] -= (y_bounds[0] - y_bounds[1])

    if point[0] < x_bounds[0] and point[1] > y_bounds[1]:
        point[0] -= (x_bounds[0] - x_bounds[1])
        point[1] += (y_bounds[1] - y_bounds[0])

    if point[0] > x_bounds[1] and point[1] > y_bounds[1]:
        point[0] += (x_bounds[0] - x_bounds[1])
        point[1] += (y_bounds[1] - y_bounds[0])

    if point[0] > x_bounds[1] and point[1] < y_bounds[0]:
        point[0] += (x_bounds[0] - x_bounds[1])
        point[1] -= (y_bounds[0] - y_bounds[1])

    if x_bounds[0] <= point[0] <= x_bounds[1]:
        if point[1] > y_bounds[1]:
            point[1] += y_bounds[0] - y_bounds[1]
        if point[1] < y_bounds[0]:
            point[1] -= y_bounds[0] - y_bounds[1]

    if y_bounds[0] <= point[1] <= y_bounds[1]:
        if point[0] > x_bounds[1]:
            point[0] += x_bounds[0] - x_bounds[1]
        if point[0] < x_bounds[0]:
            point[0] -= x_bounds[0] - x_bounds[1]

    if point[0] < x_bounds[0]:
        point[0] = x_bounds[0]
    elif point[0] > x_bounds[1]:
        point[0] = x_bounds[1]

    if point[1] < y_bounds[0]:
        point[1] = y_bounds[0]
    elif point[1] > y_bounds[1]:
        point[1] = y_bounds[1]

    return point
