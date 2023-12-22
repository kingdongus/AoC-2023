from collections import defaultdict

from toolbox.toolbox import input_file_name


def part_1(problem):
    bricks = parse_bricks(problem)

    # 'ground:' z = 0, brick min z = 1
    bricks.sort(key=lambda b: b[0][2])
    print(bricks)

    highest = defaultdict(lambda: (0, -1))  # for each column in 3d, track the highest occupied block

    cannot_be_disintegrated_safely = set()

    for idx, brick in enumerate(bricks):
        max_height = -1
        support_set = set()
        for x in range(brick[0][0], brick[1][0] + 1):
            for y in range(brick[0][1], brick[1][1] + 1):
                if highest[x, y][0] + 1 > max_height:
                    max_height = highest[x, y][0] + 1
                    support_set = {highest[x, y][1]}
                elif highest[x, y][0] + 1 == max_height:
                    support_set.add(highest[x, y][1])

        if len(support_set) == 1:
            cannot_be_disintegrated_safely.add(support_set.pop())

        # move brick down
        delta_z = brick[0][2] - max_height
        brick[0][2] -= delta_z
        brick[1][2] -= delta_z

        # update highest with new brick
        for x in range(brick[0][0], brick[1][0] + 1):
            for y in range(brick[0][1], brick[1][1] + 1):
                highest[x, y] = (brick[1][2], idx)

    return len(bricks) - len(cannot_be_disintegrated_safely) + 1


def parse_bricks(problem):
    bricks = []
    for line in problem:
        start, end = line.strip().split("~")
        bricks.append(([int(i) for i in start.split(',')], [int(i) for i in end.split(',')]))
    return bricks


def part_2(problem):
    pass


if __name__ == '__main__':
    with open(input_file_name) as problem:
        print(part_1(problem))
    with open(input_file_name) as problem:
        print(part_2(problem))
