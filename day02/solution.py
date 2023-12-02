import re

color_count_pattern = re.compile(r'\b(\d+)\s+(red|blue|green)\b')


# 12 red cubes, 13 green cubes, and 14 blue cubes
def part_1(problem):
    sum_ok = 0

    limits = {'red': 12, 'green': 13, 'blue': 14}

    for line in problem.readlines():
        matches = color_count_pattern.findall(line)
        ok = True
        for number, color in matches:
            ok = ok and limits[color] >= int(number)

        if ok:
            sum_ok += int(line.split(':')[0].split(' ')[1])  # peak engineering
    print(sum_ok)


def part_2(problem):
    sum_products = 0

    for line in problem.readlines():

        limits = {'red': 0, 'green': 0, 'blue': 0}
        matches = color_count_pattern.findall(line)

        for number, color in matches:
            limits[color] = max(limits[color], int(number))

        sum_products += limits['red'] * limits['green'] * limits['blue']
    print(sum_products)


if __name__ == '__main__':
    with open('input.txt') as problem:
        part_1(problem)
    with open('input.txt') as problem:
        part_2(problem)
