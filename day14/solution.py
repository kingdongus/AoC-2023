from toolbox.toolbox import input_file_name, read_file_into_2d_array


def part_1(problem):
    round_rocks, square_rocks = calculate_rock_layout(problem)

    # from top left to bottom right, slide all rocks up as far as possible

    tilt_north(problem, round_rocks, square_rocks)

    # calculate output

    return sum((len(problem) - x) for x, y in round_rocks)


def calculate_rock_layout(problem):
    round_rocks = []
    square_rocks = []
    for row in range(len(problem)):
        for col in range(len(problem[row])):
            if problem[row][col] == 'O':
                round_rocks.append((row, col))
            elif problem[row][col] == '#':
                square_rocks.append((row, col))
    # add fake rock layers
    for i in range(len(problem[0])):
        square_rocks.append((-1, i))
        square_rocks.append((len(problem), i))
    for i in range(len(problem)):
        square_rocks.append((i, -1))
        square_rocks.append((i, len(problem[0])))
    return round_rocks, square_rocks


def tilt_east(problem, round_rocks, square_rocks):
    for r in range(len(problem)):
        for c in range(len(problem[r]) - 1, -1, -1):
            if (r, c) in round_rocks:
                # move rock up
                rock = (r, c)
                next_rock_candidate = (r, c + 1)
                while next_rock_candidate not in round_rocks and next_rock_candidate not in square_rocks:
                    round_rocks.remove(rock)
                    round_rocks.append(next_rock_candidate)
                    rock = next_rock_candidate
                    next_rock_candidate = (rock[0], rock[1] + 1)


def tilt_west(problem, round_rocks, square_rocks):
    for r in range(len(problem)):
        for c in range(len(problem[r])):
            if (r, c) in round_rocks:
                # move rock up
                rock = (r, c)
                next_rock_candidate = (r, c - 1)
                while next_rock_candidate not in round_rocks and next_rock_candidate not in square_rocks:
                    round_rocks.remove(rock)
                    round_rocks.append(next_rock_candidate)
                    rock = next_rock_candidate
                    next_rock_candidate = (rock[0], rock[1] - 1)


def tilt_north(problem, round_rocks, square_rocks):
    for r in range(len(problem)):
        for c in range(len(problem[r])):
            if (r, c) in round_rocks:
                # move rock up
                rock = (r, c)
                next_rock_candidate = (r - 1, c)
                while next_rock_candidate not in round_rocks and next_rock_candidate not in square_rocks:
                    round_rocks.remove(rock)
                    round_rocks.append(next_rock_candidate)
                    rock = next_rock_candidate
                    next_rock_candidate = (rock[0] - 1, rock[1])


def tilt_south(problem, round_rocks, square_rocks):
    for r in range(len(problem) - 1, -1, -1):
        for c in range(len(problem[r])):
            if (r, c) in round_rocks:
                # move rock up
                rock = (r, c)
                next_rock_candidate = (r + 1, c)
                while next_rock_candidate not in round_rocks and next_rock_candidate not in square_rocks:
                    round_rocks.remove(rock)
                    round_rocks.append(next_rock_candidate)
                    rock = next_rock_candidate
                    next_rock_candidate = (rock[0] + 1, rock[1])


def part_2(problem):
    round_rocks, square_rocks = calculate_rock_layout(problem)
    cache = []
    cycles = 1_000_000_000
    for i in range(0, cycles):

        tilt_north(problem, round_rocks, square_rocks)
        tilt_west(problem, round_rocks, square_rocks)
        tilt_south(problem, round_rocks, square_rocks)
        tilt_east(problem, round_rocks, square_rocks)

        cache_hits = [c for c in cache if c[1] == round_rocks]
        if cache_hits:
            print(f"yay! after {i} cycles")
            cycles_left = cycles - i
            cycle_length = i - cache_hits[0][0]
            print(f'cycles left: {cycles_left}')
            print(f'cycle length: {cycle_length}')
            left_to_run = cycles_left % cycle_length
            for _ in range(0, left_to_run - 1):
                tilt_north(problem, round_rocks, square_rocks)
                tilt_west(problem, round_rocks, square_rocks)
                tilt_south(problem, round_rocks, square_rocks)
                tilt_east(problem, round_rocks, square_rocks)
            return calc_result(problem, round_rocks)

        else:
            cache.append((i, [row[:] for row in round_rocks]))
        if i % 1000 == 0:
            print(f'{i} cycles done')

    # calculate output
    return calc_result(problem, round_rocks)


def calc_result(problem, round_rocks):
    return sum((len(problem) - x) for x, y in round_rocks)


if __name__ == '__main__':
    field = read_file_into_2d_array(input_file_name)
    # print(part_1(field))  # 110128
    print(part_2(field))  # 110128
