import operator
import re
from functools import reduce

from toolbox.toolbox import input_file_name


def calculate_ways_to_solve(time, distance):
    # find one that beats it from one side
    first_border = 0
    for variant in range(1, time):
        remaining_time = time - variant
        if variant * remaining_time > distance:
            first_border = variant
            break
    # find another one that beats it from the other side
    second_border = 0
    for variant in range(time - 1, first_border, -1):
        remaining_time = time - variant
        if variant * remaining_time > distance:
            second_border = variant
            break

    return second_border - first_border + 1


def part_1(problem):
    times = re.sub(r'\s+', ' ', problem.readline()).split(r' ')
    distances = re.sub(r'\s+', ' ', problem.readline()).split(r' ')

    times_and_distances = [(int(a), int(b)) for a, b in dict(zip(times[1:], distances[1:])).items()]

    return reduce(operator.mul, [calculate_ways_to_solve(a, b) for a, b in times_and_distances], 1)


def part_2(problem):
    time = int(re.sub(r'\s+', '', problem.readline()).split(r':')[1])
    distance = int(re.sub(r'\s+', '', problem.readline()).split(r':')[1])

    return calculate_ways_to_solve(time, distance)


if __name__ == '__main__':
    with open(input_file_name) as problem:
        print(part_1(problem))
    with open(input_file_name) as problem:
        print(part_2(problem))
