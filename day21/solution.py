from functools import cache

from toolbox.toolbox import input_file_name, read_file_into_2d_array, in_range, directions_2d_4


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

    @cache
    def solve_for_tile(t):
        temp = []
        for d in directions_2d_4:
            candidate_row, candidate_col = (t[0] + d[0], t[1] + d[1])
            if problem[candidate_row % len(problem)][candidate_col % len(problem[0])] != '#':
                temp.append((candidate_row, candidate_col))
        return temp

    @cache
    def reachable_from_with_n_steps(starting_tiles, n):
        if n == 0:
            return starting_tiles
        tiles = set(starting_tiles)
        temp = set()
        while tiles:
            next_tile = tiles.pop()
            for t in solve_for_tile(next_tile):
                temp.add(t)
        return reachable_from_with_n_steps(tuple(temp), n - 1)

    num_steps = 500
    reachable_tiles = reachable_from_with_n_steps((start,), num_steps)

    print(solve_for_tile.cache_info())
    print(reachable_from_with_n_steps.cache_info())
    return len(reachable_tiles)


if __name__ == '__main__':
    problem = read_file_into_2d_array(input_file_name)
    print(part_1(problem))
    # print(part_2(problem)) # not done
