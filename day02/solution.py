import re


def part_2(problem):
    sum_ok = 0

    for line in problem.readlines():

        limits = {'red': 0, 'green': 0, 'blue': 0}
        pattern = re.compile(r'\b(\d+)\s+(red|blue|green)\b')
        matches = pattern.findall(line)

        for number, color in matches:
            print(limits)
            print(f'{color}, {number}')
            limits[color] = max(limits[color], int(number))

        sum_ok += limits['red'] * limits['green'] * limits['blue']
    print(sum_ok)  # 1683 bad


# 12 red cubes, 13 green cubes, and 14 blue cubes
def part_1(problem):
    sum_ok = 0

    limits = {'red': 12, 'green': 13, 'blue': 14}

    for line in problem.readlines():
        lr = line.split(':')
        game_nr = lr[0].split(' ')[1]

        pattern = re.compile(r'\b(\d+)\s+(red|blue|green)\b')
        matches = pattern.findall(line)

        ok = True
        for number, color in matches:
            # print(f'number {number}, color {color}')
            ok = ok and limits[color] >= int(number)
            # print(f'limit[{color}]: {limits[color]}, {number}')

        if ok:
            sum_ok += int(game_nr)
    print(sum_ok)  # 1683 bad


if __name__ == '__main__':
    with open('input.txt') as problem:
        part_2(problem)
