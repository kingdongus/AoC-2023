import re

from toolbox.toolbox import input_file_name


def part_1(problem):
    times = re.sub(r'\s+', ' ', problem.readline()).split(r' ')
    distances = re.sub(r'\s+', ' ', problem.readline()).split(r' ')

    times_and_distances = [(int(a), int(b)) for a, b in dict(zip(times[1:], distances[1:])).items()]

    total_ways_to_beat = 1

    for time, distance in times_and_distances:
        ways_to_beat = 0
        for variant in range(1, time):
            remaining_time = time - variant
            if variant * remaining_time > distance:
                ways_to_beat += 1
        total_ways_to_beat *= ways_to_beat

    return total_ways_to_beat


def part_2(problem):
    time = int(re.sub(r'\s+', '', problem.readline()).split(r':')[1])
    distance = int(re.sub(r'\s+', '', problem.readline()).split(r':')[1])

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


if __name__ == '__main__':
    with open(input_file_name) as problem:
        print(part_1(problem))
    with open(input_file_name) as problem:
        print(part_2(problem))
