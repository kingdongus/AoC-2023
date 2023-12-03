directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]


def read_file_into_2d_array(file_path):
    try:
        # Open the file for reading
        with open(file_path, 'r') as file:
            lines = file.readlines()

            two_d_array = []

            for line in lines:
                values = list(line)
                two_d_array.append(values)

            return two_d_array
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return None


def part_1(problem):
    as_array = read_file_into_2d_array('input.txt')
    numbers = [str(i) for i in range(10)]

    gear_sum = 0

    for y in range(len(as_array)):
        for x in range(len(as_array[y])):
            if as_array[y][x] not in numbers and as_array[y][x] not in ['.', '\n']:
                # check in all directions to see if we find numbers
                for direction in directions:
                    direction_new_x = x + direction[0]
                    direction_new_y = y + direction[1]
                    if direction_new_x > -1 and direction_new_x < len(
                            as_array[y]) and direction_new_y > -1 and direction_new_y < len(as_array) and \
                            as_array[direction_new_y][direction_new_x] in numbers:
                        # expand and erase number
                        ny = direction_new_y
                        nx = direction_new_x

                        # move left until you don't find a number anymore
                        while nx > -1 and as_array[ny][nx - 1] in numbers:
                            nx -= 1
                        # move right until you don't find a number anymore
                        num = as_array[ny][nx]
                        as_array[ny][nx] = '.'

                        while nx < len(as_array[y]) and as_array[ny][nx + 1] in numbers:
                            nx += 1
                            num += as_array[ny][nx]
                            as_array[ny][nx] = '.'
                        print(num)

                        gear_sum += int(num)
    print(gear_sum)


def part_2(problem):
    as_array = read_file_into_2d_array('input.txt')
    numbers = [str(i) for i in range(10)]

    gear_ratio_product = 0

    for y in range(len(as_array)):
        for x in range(len(as_array[y])):
            if as_array[y][x] == '*':
                # check in all directions to see if we find numbers
                surrounding_numbers = []
                for direction in directions:
                    direction_new_x = x + direction[0]
                    direction_new_y = y + direction[1]
                    if direction_new_x > -1 and direction_new_x < len(
                            as_array[y]) and direction_new_y > -1 and direction_new_y < len(as_array) and \
                            as_array[direction_new_y][direction_new_x] in numbers:
                        # expand number
                        ny = direction_new_y
                        nx = direction_new_x

                        # move left until you don't find a number anymore
                        while nx > -1 and as_array[ny][nx - 1] in numbers:
                            nx -= 1
                        # move right until you don't find a number anymore
                        num = as_array[ny][nx]
                        as_array[ny][nx] = '.'

                        while nx < len(as_array[y]) and as_array[ny][nx + 1] in numbers:
                            nx += 1
                            num += as_array[ny][nx]
                            as_array[ny][nx] = '.'
                        print(num)
                        surrounding_numbers.append(num)

                if len(surrounding_numbers) == 2:
                    print(surrounding_numbers)
                    gear_ratio_product += int(surrounding_numbers[0]) * int(surrounding_numbers[1])
    print(gear_ratio_product)


if __name__ == '__main__':
    with open('input.txt') as problem:
        part_1(problem)
    with open('input.txt') as problem:
        part_2(problem)
