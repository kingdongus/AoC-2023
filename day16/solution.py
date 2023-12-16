from toolbox.toolbox import input_file_name, read_file_into_2d_array, direction_east, in_range, direction_north, \
    direction_south, direction_west


def calc_for(problem, start):
    energized = {start}
    rays = [start]
    memory = set()

    while rays:
        location, direction = rays.pop()

        if not in_range(location[0], problem) or not in_range(location[1], problem[0]):
            continue
        if (location, direction) in memory:
            continue

        memory.add((location, direction))
        energized.add(location)
        new_location = (location[0] + direction[0], location[1] + direction[1])

        if not in_range(new_location[0], problem) or not in_range(new_location[1], problem[0]):
            continue

        tile = problem[new_location[0]][new_location[1]]
        if tile == '.':
            rays.append((new_location, direction))
        elif tile == '/':
            if direction == direction_north:
                rays.append((new_location, direction_east))
            elif direction == direction_east:
                rays.append((new_location, direction_north))
            elif direction == direction_south:
                rays.append((new_location, direction_west))
            elif direction == direction_west:
                rays.append((new_location, direction_south))
        elif tile == '\\':
            if direction == direction_north:
                rays.append((new_location, direction_west))
            elif direction == direction_east:
                rays.append((new_location, direction_south))
            elif direction == direction_south:
                rays.append((new_location, direction_east))
            elif direction == direction_west:
                rays.append((new_location, direction_north))
        elif tile == '-':
            if direction == direction_north or direction == direction_south:
                rays.append((new_location, direction_east))
                rays.append((new_location, direction_west))
            else:
                rays.append((new_location, direction))
        elif tile == '|':
            if direction == direction_east or direction == direction_west:
                rays.append((new_location, direction_north))
                rays.append((new_location, direction_south))
            else:
                rays.append((new_location, direction))

    return len(energized) - 1  # not sure where this comes from 🤡


def part_1(problem):
    start = ((0, 0), direction_east)
    return calc_for(problem, start)


def part_2(problem):
    starting_points = [((0, x), direction_south) for x in range(len(problem[0]))] + [
        ((len(problem) - 1, x), direction_north) for x in range(len(problem[0]))] + [
                          ((x, 0), direction_east) for x in range(len(problem))] + [
                          ((x, len(problem[0]) - 1), direction_west) for x in range(len(problem))]
    return max((calc_for(problem, x)) for x in starting_points)


if __name__ == '__main__':
    problem = read_file_into_2d_array(input_file_name)
    print(part_1(problem))
    print(part_2(problem))
