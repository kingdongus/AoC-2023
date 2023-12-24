from collections import namedtuple

from toolbox.toolbox import input_file_name

Hailstone = namedtuple('Hailstone', ['x', 'y', 'z'])
Velocity = namedtuple('Velocity', ['x', 'y', 'z'])


def part_1(problem):
    hailstones_and_velocities = []
    for line in problem:
        raw_position, raw_velocity = line.split(' @ ')
        raw_position = [int(x.strip()) for x in raw_position.split(',')]
        raw_velocity = [int(x.strip()) for x in raw_velocity.split(',')]
        hailstone = Hailstone(raw_position[0], raw_position[1], raw_position[2])
        velocity = Velocity(raw_velocity[0], raw_velocity[1], raw_velocity[2])
        hailstones_and_velocities.append((hailstone, velocity))

    # x AND y
    test_area_start = 200000000000000
    test_area_end = 400000000000000

    intersections = {h[0]: set() for h in hailstones_and_velocities}
    num_intersects = 0
    checked = set()

    for h1, v1 in hailstones_and_velocities:
        for h2, v2 in hailstones_and_velocities:
            if h1 == h2:
                continue

            s = tuple(sorted([h1, h2], key=lambda h: h.x))
            if s in checked:
                continue
            checked.add(s)

            print('\n')
            # y = mx + b
            slope_h1 = v1.y / v1.x
            slope_h2 = v2.y / v2.x

            # same line or parallel
            if slope_h1 == slope_h2:
                print(f'Hailstone A: {h1}, {v1}')
                print(f'Hailstone B: {h2}, {v2}')
                print('parallel, no intersection')
                continue

            y_intercept1 = h1.y - (slope_h1 * h1.x)
            y_intercept2 = h2.y - (slope_h2 * h2.x)

            print(f'Hailstone A: {h1}, {v1}')
            print(f'Hailstone B: {h2}, {v2}')

            intersect_x = (y_intercept2 - y_intercept1) / (slope_h1 - slope_h2)
            intersect_y = slope_h1 * intersect_x + y_intercept1
            print(f'intersecting at {intersect_x}, {intersect_y}')

            if not test_area_start <= intersect_x <= test_area_end or not test_area_start <= intersect_y <= test_area_end:
                print('intersection outside of test area')
                continue

            if h1.x < intersect_x and v1.x <= 0 or h1.y < intersect_y and v1.y <= 0 \
                    or h1.x > intersect_x and v1.x >= 0 or h1.y > intersect_y and v1.y >= 0:
                print('intersection in the past for hailstone a')
                continue
            if h2.x < intersect_x and v2.x <= 0 or h2.y < intersect_y and v2.y <= 0 \
                    or h2.x > intersect_x and v2.x >= 0 or h2.y > intersect_y and v2.y >= 0:
                print('intersection in the past for hailstone b')
                continue

            intersections[h1].add((intersect_x, intersect_y))
            num_intersects += 1

    return num_intersects


def part_2(problem):
    pass


if __name__ == '__main__':
    with open(input_file_name) as problem:
        print(part_1(problem))
    with open(input_file_name) as problem:
        print(part_2(problem))
