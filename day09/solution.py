from toolbox.toolbox import input_file_name


def continue_series(series):
    history = [series]

    pairs = [(series[x], series[x + 1]) for x in range(len(series) - 1)]
    deltas = [b - a for a, b in pairs]

    while not deltas.count(0) == len(deltas):
        history = [deltas] + history
        pairs = [(deltas[x], deltas[x + 1]) for x in range(len(deltas) - 1)]
        deltas = [b - a for a, b in pairs]

    return sum(s[-1] for s in history)


def part_1(problem):
    return sum(continue_series([int(x) for x in line.split(' ')]) for line in problem)


def part_2(problem):
    return sum(continue_series(list(reversed([int(x) for x in line.split(' ')]))) for line in problem)


if __name__ == '__main__':
    with open(input_file_name) as problem:
        print(part_1(problem))
    with open(input_file_name) as problem:
        print(part_2(problem))
