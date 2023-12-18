import re

from toolbox.toolbox import input_file_name, direction_north, direction_west, direction_east, direction_south, \
    directions_2d_8

direction_to_coord = {
    'U': direction_north,
    'D': direction_south,
    'L': direction_west,
    'R': direction_east,
}


def part_1(problem):
    instructions = []
    for line in problem:
        s = line.strip().split(' ')
        direction, distance, color = s[0], s[1], s[2]
        instructions.append((direction, int(distance), color))

    return calculate_lagoon_2(instructions)


def calculate_lagoon(instructions):
    current = (0, 0)
    visited = set()
    visited.add(current)
    for direction, distance, _ in instructions:
        for d in range(distance):
            current = current[0] + direction_to_coord[direction][0], current[1] + direction_to_coord[direction][1]
            visited.add(current)
    # flood fill
    work = [(1, 1)]
    c = 0
    while work:
        c += 1
        if c % 1000000 == 0:
            print(f'processed: {c}')
        n = work.pop()
        visited.add(n)
        for d in directions_2d_8:
            candidate = n[0] + d[0], n[1] + d[1]
            if candidate not in visited:
                work.append(candidate)
    return len(visited)


def calculate_lagoon_2(instructions):
    current = (0, 0)
    visited = set()
    visited.add(current)
    for direction, distance, _ in instructions:
        for d in range(distance):
            current = current[0] + direction_to_coord[direction][0], current[1] + direction_to_coord[direction][1]
            visited.add(current)
    # calculate per 'row'
    visited = list(sorted(visited))
    row_idx = 0
    row = [x for x in visited if x[0] == row_idx]
    while row:
        # todo
        print(row_idx, row)
        row_idx += 1
        row = [x for x in visited if x[0] == row_idx]


def extract_hex_number(input_string):
    pattern = re.compile(r'#([0-9a-fA-F]+)')
    match = pattern.search(input_string)

    if match:
        return match.group(1)
    else:
        return None


hex_digit_to_direction = {
    '0': 'R',
    '1': 'D',
    '2': 'L',
    '3': 'U'
}


def part_2(problem):
    instructions = []
    for line in problem:
        s = line.strip().split(' ')
        _, _, color = s[0], s[1], s[2]
        h = extract_hex_number(color)
        instructions.append((hex_digit_to_direction[h[-1]], int(h[:5], 16), color))

    return calculate_lagoon_2(instructions)


if __name__ == '__main__':
    # with open(input_file_name) as problem:
    #     print(part_1(problem))
    with open(input_file_name) as problem:
        print(part_2(problem))
