from toolbox.toolbox import input_file_name


def hash_block(block):
    res = 0
    for c in list(block):
        print(c)
        res += ord(c)
        res *= 17
        res %= 256
    return res


def part_1(problem):
    return sum(hash_block(block) for block in problem.readline().strip().split(','))


def part_2(problem):
    # key: int, value: [box label, focal length]
    boxes = {i: [] for i in range(256)}

    for block in problem.readline().strip().split(','):
        if '=' in block:
            # add
            lens_label, focal_length = block.split('=')
            box = hash_block(lens_label)
            found_match = False
            for l in boxes[box]:
                if l[0] == lens_label:
                    l[1] = focal_length
                    found_match = True
                    break
            if not found_match:
                boxes[box].append([lens_label, focal_length])

        elif '-' in block:
            # remove
            lens_label = block.split('-')[0]
            box = hash_block(lens_label)
            lenses_for_box = boxes[box]
            for i in range(len(lenses_for_box)):
                if lenses_for_box[i][0] == lens_label:
                    del lenses_for_box[i]
                    break

    total_focusing_power = 0
    for box_number, lenses in boxes.items():
        for i in range(len(lenses)):
            total_focusing_power += (1 + box_number) * (i + 1) * int(lenses[i][1])
    return total_focusing_power


def calc_result(problem, round_rocks):
    return sum((len(problem) - x) for x, y in round_rocks)


if __name__ == '__main__':
    with open(input_file_name) as problem:
        print(part_1(problem))
    with open(input_file_name) as problem:
        print(part_2(problem))
