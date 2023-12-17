from heapq import heappush, heappop

from toolbox.toolbox import input_file_name, read_file_into_2d_array, direction_south, \
    direction_north, direction_west, direction_east, in_range, directions_2d_4

opposites = {
    direction_north: direction_south,
    direction_south: direction_north,
    direction_east: direction_west,
    direction_west: direction_east,
}


def traverse(city):
    seen = set()
    work = [(0, (0, 0), direction_east, 0), (0, (0, 0), direction_south, 0)]

    while work:
        heat, position, direction, direction_count = heappop(work)
        if (position, direction, direction_count) in seen:
            continue
        seen.add((position, direction, direction_count))

        new_row, new_col = position[0] + direction[0], position[1] + direction[1]
        if not in_range(new_col, city) or not in_range(new_row, city[0]):
            continue
        new_heat = heat + city[new_col][new_row]
        if direction_count < 4:
            if new_col == len(city) - 1 and new_row == len(city[0]) - 1:
                return new_heat
        for d in directions_2d_4:
            if d == opposites[direction]:
                continue
            new_direction_count = direction_count + 1 if d == direction else 1
            if new_direction_count > 3:
                continue
            heappush(work, (new_heat, (new_row, new_col), d, new_direction_count))


def part_1(problem):
    return traverse(problem)


def part_2(problem):
    pass


if __name__ == '__main__':
    problem = read_file_into_2d_array(input_file_name)
    for i in range(len(problem)):
        for j in range(len(problem[0])):
            problem[i][j] = int(problem[i][j])
    print(part_1(problem))
    print(part_2(problem))
