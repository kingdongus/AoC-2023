from functools import reduce

number_strings = [str(i) for i in range(10)]
directions_2d_8 = [(x, y) for x in [-1, 0, 1] for y in [-1, 0, 1] if not (x == 0 and y == 0)]
directions_2d_4 = [(1, 0), (-1, 0), (0, 1), (0, -1)]

input_file_name = 'input.txt'


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
