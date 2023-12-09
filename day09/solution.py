from toolbox.toolbox import input_file_name


def continue_series(series):
    history = [series]

    pairs = [(series[x], series[x + 1]) for x in range(len(series) - 1)]
    deltas = [b - a for a, b in pairs]

    while not deltas.count(0) == len(deltas):
        history = [deltas] + history
        tmp = deltas
        pairs = [(tmp[x], tmp[x + 1]) for x in range(len(tmp) - 1)]
        deltas = [b - a for a, b in pairs]

    increment_by = 0
    while history:
        next_series = history.pop()
        increment_by = next_series[-1] + increment_by

    return increment_by


def part_1(problem):
    return sum(continue_series([int(x) for x in line.split(' ')]) for line in problem)


def part_2(problem):
    return sum(continue_series(list(reversed([int(x) for x in line.split(' ')]))) for line in problem)


if __name__ == '__main__':
    with open(input_file_name) as problem:
        print(part_1(problem))
    with open(input_file_name) as problem:
        print(part_2(problem))
