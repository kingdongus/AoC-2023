from heapq import heappush, heappop

from toolbox.toolbox import input_file_name, read_file_into_2d_array, direction_south, \
    direction_north, direction_west, direction_east, in_range, directions_2d_4

opposites = {
    direction_north: direction_south,
    direction_south: direction_north,
    direction_east: direction_west,
    direction_west: direction_east,
}


def traverse_2(city, min_step, max_step):
    seen = set()
    work = [(0, (0, 0), direction_east, 1), (0, (0, 0), direction_south, 1)]

    while work:
        heat_loss, position, direction, consecutive_steps = heappop(work)
        if (position, direction, consecutive_steps) in seen:
            continue
        seen.add((position, direction, consecutive_steps))

        new_row, new_col = position[0] + direction[0], position[1] + direction[1]
        if not in_range(new_col, city) or not in_range(new_row, city[0]):
            continue
        new_heat_loss = heat_loss + city[new_col][new_row]
        if min_step <= consecutive_steps <= max_step:
            if new_col == len(city) - 1 and new_row == len(city[0]) - 1:
                return new_heat_loss
        for new_direction in directions_2d_4:
            if new_direction == opposites[direction]:
                continue
            new_direction_count = consecutive_steps + 1 if new_direction == direction else 1
            if (
                    direction != new_direction and consecutive_steps < min_step) or new_direction_count > max_step:  # need to move at least min_step consecutive_steps in a straight line before one can turn
                continue
            heappush(work, (new_heat_loss, (new_row, new_col), new_direction, new_direction_count))


def part_1(problem):
    return traverse_2(problem, 1, 3)


def part_2(problem):
    return traverse_2(problem, 4, 10)


if __name__ == '__main__':
    problem = read_file_into_2d_array(input_file_name)
    for i in range(len(problem)):
        for j in range(len(problem[0])):
            problem[i][j] = int(problem[i][j])
    print(part_1(problem))
    print(part_2(problem))
