from toolbox.toolbox import input_file_name, read_file_into_2d_array, in_range, directions_2d_4, calculate_quadratic_fit


def part_1(problem):
    start = None
    for row in range(len(problem)):
        for col in range(len(problem[0])):
            if problem[row][col] == 'S':
                start = (row, col)

    reachable_tiles = {start}
    num_steps = 64

    for _ in range(num_steps):
        temp = set()
        while reachable_tiles:
            next_tile = reachable_tiles.pop()
            for d in directions_2d_4:
                candidate_row, candidate_col = (next_tile[0] + d[0], next_tile[1] + d[1])
                if (in_range(candidate_row, problem)
                        and in_range(candidate_col, problem[0])
                        and problem[candidate_row][candidate_col] != '#'):
                    temp.add((candidate_row, candidate_col))
        reachable_tiles = temp

    return len(reachable_tiles)


def part_2(problem):
    start = None
    for row in range(len(problem)):
        for col in range(len(problem[0])):
            if problem[row][col] == 'S':
                start = (row, col)

    def count_reachable_from_with_n_steps_across_borders(n):
        reachable_tiles = {start}
        for _ in range(n):
            temp = set()
            while reachable_tiles:
                next_tile = reachable_tiles.pop()
                for d in directions_2d_4:
                    candidate_row, candidate_col = (next_tile[0] + d[0], next_tile[1] + d[1])
                    if problem[candidate_row % len(problem)][candidate_col % len(problem[0])] != '#':
                        temp.add((candidate_row, candidate_col))
            reachable_tiles = temp
        return len(reachable_tiles)

    len_input_grid = len(problem)

    points = [(i, count_reachable_from_with_n_steps_across_borders(len_input_grid // 2 + i * len_input_grid)) for i in
              range(3)]

    num_steps = 26501365
    return calculate_quadratic_fit(points, num_steps // len_input_grid)


if __name__ == '__main__':
    problem = read_file_into_2d_array(input_file_name)
    print(part_1(problem))
    print(part_2(problem))
