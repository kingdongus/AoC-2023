from toolbox.toolbox import read_file_into_2d_array, directions, number_strings, in_range


def part_1(problem):
    numbers = [str(i) for i in range(10)]

    gear_sum = 0

    for y in range(len(problem)):
        for x in range(len(problem[y])):
            if problem[y][x] not in numbers and problem[y][x] not in ['.', '\n']:
                # check in all directions to see if we find numbers
                for direction in directions:
                    direction_new_x = x + direction[0]
                    direction_new_y = y + direction[1]
                    if in_range(direction_new_x, problem[y]) and in_range(direction_new_y, problem) and \
                            problem[direction_new_y][direction_new_x] in numbers:
                        # expand and erase number
                        ny = direction_new_y
                        nx = direction_new_x

                        # move left until you don't find a number anymore
                        while in_range(nx, problem[y]) and problem[ny][nx - 1] in numbers:
                            nx -= 1
                        # move right until you don't find a number anymore
                        num = problem[ny][nx]
                        problem[ny][nx] = '.'

                        while in_range(nx, problem[y]) and problem[ny][nx + 1] in numbers:
                            nx += 1
                            num += problem[ny][nx]
                            problem[ny][nx] = '.'

                        gear_sum += int(num)
    return gear_sum


def part_2(problem):
    gear_ratio_product = 0

    for y in range(len(problem)):
        for x in range(len(problem[y])):
            if problem[y][x] == '*':
                # check in all directions to see if we find numbers
                surrounding_numbers = []
                for direction in directions:
                    direction_new_x = x + direction[0]
                    direction_new_y = y + direction[1]
                    if in_range(direction_new_x, problem[y]) and in_range(direction_new_y, problem) and \
                            problem[direction_new_y][direction_new_x] in number_strings:
                        # expand number
                        ny = direction_new_y
                        nx = direction_new_x

                        # move left until you don't find a number anymore
                        while in_range(nx, problem[y]) and problem[ny][nx - 1] in number_strings:
                            nx -= 1
                        # move right until you don't find a number anymore
                        num = problem[ny][nx]
                        problem[ny][nx] = '.'

                        while in_range(nx, problem[y]) and problem[ny][nx + 1] in number_strings:
                            nx += 1
                            num += problem[ny][nx]
                            problem[ny][nx] = '.'
                        surrounding_numbers.append(num)

                if len(surrounding_numbers) == 2:
                    gear_ratio_product += int(surrounding_numbers[0]) * int(surrounding_numbers[1])
    return gear_ratio_product


if __name__ == '__main__':
    print(part_1(read_file_into_2d_array('input.txt')))
    print(part_2(read_file_into_2d_array('input.txt')))
