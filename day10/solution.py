import toolbox.toolbox
from toolbox.toolbox import input_file_name, in_range
from toolbox.toolbox import read_file_into_2d_array

connections_per_pipe = {
    '|': [(1, 0), (-1, 0)],
    '-': [(0, 1), (0, -1)],
    'L': [(-1, 0), (0, 1)],
    'J': [(-1, 0), (0, -1)],
    '7': [(1, 0), (0, -1)],
    'F': [(1, 0), (0, 1)],
    '.': [],
    'S': toolbox.toolbox.directions_2d_8[::],
}


def follow_path_and_record_length(previous, current, map):
    depth = 0

    while True:
        current_pipe = map[current[0]][current[1]]
        if current_pipe == 'S':
            return depth
        directions = connections_per_pipe[current_pipe];
        candidates = [(current[0] + d[0], current[1] + d[1]) for d in directions]
        candidates = [candidate for candidate in candidates if candidate != previous
                      and in_range(candidate[0], map) and in_range(candidate[1], map[1])]

        if not candidates:
            return -1

        previous, current = current, candidates[0]
        depth += 1


def follow_and_memorize_path(previous, current, tiles):
    path = [previous, current]
    while True:
        current_pipe = tiles[current[0]][current[1]]
        if current_pipe == 'S':
            return path
        candidates = [(current[0] + d[0], current[1] + d[1]) for d in (connections_per_pipe[current_pipe])]
        candidates = [candidate for candidate in candidates if candidate != previous
                      and in_range(candidate[0], tiles) and in_range(candidate[1], tiles[1])]

        if not candidates:
            return []

        previous, current = current, candidates[0]
        path.append(candidates[0])


def find_start(problem):
    for row_idx in range(len(problem)):
        for col_idx in range(len(problem[0])):
            if problem[row_idx][col_idx] == 'S':
                return row_idx, col_idx


def part_1(problem):
    start = find_start(problem)
    return max(
        [follow_path_and_record_length(start, (start[0] + d[0], start[1] + d[1]), problem) for d in
         toolbox.toolbox.directions_2d_4]) // 2 + 1


def part_2(problem):
    start = find_start(problem)
    for direction in connections_per_pipe['S']:
        # check whether a surrounding tile actually connects to start
        adjacent_x = start[0] + direction[0]
        adjacent_y = start[1] + direction[1]
        if start not in [(adjacent_x + d[0], adjacent_y + d[1]) for d in
                         connections_per_pipe[problem[adjacent_x][adjacent_y]]]:
            continue

        adjacent = (adjacent_x, adjacent_y)
        loop_tiles = follow_and_memorize_path(start, adjacent, problem)
        if loop_tiles:
            break

    cleanup_bad_pipes(loop_tiles, problem)
    problem[start[0]][start[1]] = find_replacement_for_start(loop_tiles, problem, start)

    count = 0
    # crossing
    for row in range(len(problem)):
        crossed = 0
        for col in range(len(problem[0])):
            if problem[row][col] in list('|LJ'):
                crossed += 1
            elif problem[row][col] == '.':
                if crossed % 2 == 1:
                    count += 1
    return count


def cleanup_bad_pipes(loop_tiles, problem):
    for row in range(len(problem)):
        for col in range(len(problem[0])):
            if (row, col) not in loop_tiles:
                problem[row][col] = '.'


def find_replacement_for_start(loop_tiles, problem, start):
    has_incoming_left = (start[0], start[1] - 1) in loop_tiles and problem[start[0]][start[1] - 1] in list('-LF')
    has_incoming_right = (start[0], start[1] + 1) in loop_tiles and problem[start[0]][start[1] + 1] in list('-J7')
    has_incoming_top = (start[0] - 1, start[1]) in loop_tiles and problem[start[0] - 1][start[1]] in list('7F|')
    has_incoming_bottom = (start[0] + 1, start[1]) in loop_tiles and problem[start[0] + 1][start[1]] in list('|LJ')
    replacement = '.'
    if has_incoming_top and has_incoming_right:
        replacement = 'L'
    elif has_incoming_top and has_incoming_bottom:
        replacement = '|'
    elif has_incoming_left and has_incoming_right:
        replacement = '-'
    elif has_incoming_top and has_incoming_left:
        replacement = 'J'
    elif has_incoming_bottom and has_incoming_left:
        replacement = '7'
    elif has_incoming_bottom and has_incoming_right:
        replacement = 'F'
    return replacement


if __name__ == '__main__':
    problem = read_file_into_2d_array(input_file_name)
    print(part_1(problem))
    print(part_2(problem))  # 120 too low, 240 too low
