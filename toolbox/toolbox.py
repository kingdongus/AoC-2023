from functools import reduce

import numpy as np

number_strings = [str(i) for i in range(10)]

direction_north = (-1, 0)
direction_west = (0, -1)
direction_south = (1, 0)
direction_east = (0, 1)

directions_2d_4 = [direction_north, direction_east, direction_south, direction_west]
directions_2d_8 = [(x, y) for x in [-1, 0, 1] for y in [-1, 0, 1] if not (x == 0 and y == 0)]

input_file_name = 'input.txt'


# needs n+1 points to fit polynomial of degree n
def calculate_quadratic_fit(points, x):
    coefficients = np.polyfit(*zip(*points), 2)
    return round(np.polyval(coefficients, x))


def shoelace(points):
    return sum((i[0] + j[0]) * (i[1] - j[1]) for i, j in zip(points, points[1:] + points[:1])) // 2


def manhattan_distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def read_file_into_2d_array(file_path):
    try:
        with open(file_path, 'r') as file:
            return [list(line.replace('\n', '')) for line in file.readlines()]
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return None


def in_range(index, array):
    return -1 < index < len(array)


def transpose_list_of_strings(chunk):
    transposed = []
    for i in range(len(chunk[0])):
        transposed.append(''.join([x[i] for x in chunk]))
    return transposed


def gcd(a, b):
    """Return greatest common divisor using Euclid's Algorithm."""
    while b:
        a, b = b, a % b
    return a


def lcm(a, b):
    """Return lowest common multiple."""
    return a * b // gcd(a, b)


def lcmm(*args):
    """Return lcm of args."""
    return reduce(lcm, args)
