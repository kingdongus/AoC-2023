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
    'S': [direction for direction in toolbox.toolbox.directions_2d_8],
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


def follow_and_memorize_path(previous, current, map):
    path = [previous, current]
    while True:
        current_pipe = map[current[0]][current[1]]
        if current_pipe == 'S':
            return path
        candidates = [(current[0] + d[0], current[1] + d[1]) for d in (connections_per_pipe[current_pipe])]
        candidates = [candidate for candidate in candidates if candidate != previous
                      and in_range(candidate[0], map) and in_range(candidate[1], map[1])]
        print(current, current_pipe, connections_per_pipe[current_pipe], candidates)

        if not candidates:
            return []

        previous, current = current, candidates[0]
        path.append(candidates[0])


def find_start(problem):
    start = (-1, -1)
    for row_idx in range(len(problem)):
        for col_idx in range(len(problem[0])):
            if problem[row_idx][col_idx] == 'S':
                start = (row_idx, col_idx)
                break
    return start


def part_1(problem):
    start = find_start(problem)
    return max(
        [follow_path_and_record_length(start, (start[0] + d[0], start[1] + d[1]), problem) for d in
         toolbox.toolbox.directions_2d_4]) // 2 + 1


def part_2(problem):
    start = find_start(problem)
    print(f"start: {start}")
    for direction in [(0, 1)]:
        loop_tiles = follow_and_memorize_path(start, (start[0] + direction[0], start[1] + direction[1]), problem)
        if loop_tiles:
            break
    print(f'path length: {len(loop_tiles)}')

    # cleanup bad pipes
    for row in range(len(problem)):
        for col in range(len(problem[0])):
            if (row, col) not in loop_tiles:
                problem[row][col] = '.'

    for row in problem:
        print(''.join(row))

    # replace s
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

    problem[start[0]][start[1]] = replacement

    count = 0
    # crossing
    for row in range(len(problem)):
        crossed = 0
        for col in range(len(problem[0])):
            found = False
            if problem[row][col] in list('|LJ'):
                crossed += 1
            elif problem[row][col] == '.':
                if crossed % 2 == 1:
                    found = True
                    count += 1
                    problem[row][col] = 'X'
            if not found:
                problem[row][col] = ' '

    for row in problem:
        print(''.join(row))
    return count


if __name__ == '__main__':
    problem = read_file_into_2d_array(input_file_name)
    print(part_1(problem))
    print(part_2(problem))  # 120 too low, 240 too low
