from toolbox.toolbox import input_file_name, read_file_into_2d_array


def part_1(problem):
    # take note of all round rocks
    # take note of all square rocks

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

    # from top left to bottom right, slide all rocks up as far as possible

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

    # calculate output

    return sum((len(problem) - x) for x, y in round_rocks)


def part_2(problem):
    pass


if __name__ == '__main__':
    field = read_file_into_2d_array(input_file_name)
    print(part_1(field))  # 110128
