from itertools import combinations

from toolbox.toolbox import input_file_name, read_file_into_2d_array, manhattan_distance


def expand_observation(problem):
    expanded_cols = []
    for c in range(len(problem)):
        expanded_cols.append([])

    # columns
    for row in range(len(problem[0])):
        col = ''.join([problem[x][row] for x in range(len(problem))])
        print(col)
        if not '#' in col:
            for i in range(len(col)):
                expanded_cols[i].append('.')
                expanded_cols[i].append('.')
        else:
            for i in range(len(col)):
                expanded_cols[i].append(col[i])

    expanded_rows = []

    # rows
    for row in expanded_cols:
        if not '#' in row:
            expanded_rows.append(row)
            expanded_rows.append(row)
        else:
            expanded_rows.append(row)

    return expanded_rows


def expand_observation_part_2(problem):
    empty_cols = []
    empty_rows = []

    # columns
    for row in range(len(problem[0])):
        col = ''.join([problem[x][row] for x in range(len(problem))])
        if '#' not in col:
            empty_cols.append(row)

    # rows
    for row in range(len(problem)):
        if '#' not in problem[row]:
            empty_rows.append(row)

    return empty_rows, empty_cols


def part_1(problem):
    expanded = expand_observation(problem)
    print(f'problem: {print_observation(problem)}')
    print(f'expanded: {print_observation(expanded)}')

    galaxies = []
    for row in range(len(expanded)):
        for col in range(len(expanded[0])):
            if expanded[row][col] == "#":
                galaxies.append((row, col))
    pairwise = combinations(galaxies, 2)

    return sum([manhattan_distance(x[0], x[1]) for x in pairwise])


def part_2(problem):
    empty_rows, empty_cols = expand_observation_part_2(problem)
    print(empty_rows)
    print(empty_cols)
    weight = 1000000

    # calculate distance normally, then add weight - 1 for each crossing of an empty row or col
    galaxies = []
    for row in range(len(problem)):
        for col in range(len(problem[0])):
            if problem[row][col] == "#":
                galaxies.append((row, col))
    pairwise = combinations(galaxies, 2)

    total_distance = 0

    for pair in pairwise:
        distance = manhattan_distance(pair[0], pair[1])
        empty_rows_crossed = len(
            [r for r in empty_rows if min(pair[0][0], pair[1][0]) < r < max(pair[0][0], pair[1][0])])
        empty_cols_crossed = len(
            [r for r in empty_cols if min(pair[0][1], pair[1][1]) < r < max(pair[0][1], pair[1][1])])
        distance += (empty_cols_crossed + empty_rows_crossed) * (weight - 1)
        total_distance += distance

    return total_distance


def print_observation(galaxy):
    for row in galaxy:
        print(''.join(row))


if __name__ == '__main__':
    problem = read_file_into_2d_array(input_file_name)
    # print(part_1(problem))
    print(part_2(problem))
