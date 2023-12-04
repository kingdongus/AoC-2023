import re

from toolbox.toolbox import input_file_name


def extract_lists(input_string):
    pattern = r'Card *\d+: *(\d+(?: *\d+)*) \| *(\d+(?: *\d+)*)'
    match = re.search(pattern, input_string)

    if match:
        list1 = [int(num) for num in match.group(1).split()]
        list2 = [int(num) for num in match.group(2).split()]

        return list1, list2
    else:
        return None


def part_1(problem):
    score = 0

    for line in problem:
        lists = extract_lists(line)
        len_intersection = len(list(set(lists[0]) & set(lists[1])))
        score += 2 ** (len_intersection - 1) if len_intersection else 0

    return score


def part_2(problem, line_count):
    copies = {x: 1 for x in range(line_count)}
    idx = 0
    for line in problem:
        lists = extract_lists(line)
        intersection = list(set(lists[0]) & set(lists[1]))

        for i in range(idx + 1, idx + len(intersection) + 1):
            if copies[i] is not None:
                copies[i] += copies[idx]

        idx += 1

    return sum(x for _, x in copies.items())


if __name__ == '__main__':
    with open(input_file_name) as problem:
        print(part_1(problem))
    line_count = len(open(input_file_name).readlines())
    with open(input_file_name) as problem:
        print(part_2(problem, line_count))
