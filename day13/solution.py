from toolbox.toolbox import input_file_name, transpose_list_of_strings


def find_candidates(line):
    candidates = []
    for i in range(1, len(line)):
        left, right = line[0:i], line[i:len(line)]
        to_compare_length = min(len(left), len(right))
        left, right = left[-to_compare_length:], right[:to_compare_length]
        if left == right[::-1]:
            candidates += [i]
    return candidates


def find_vertical_axis(chunk):
    # idea: we individually calc candidates for potential mirror axis,
    # and memorize the one index that needs to be a candidate for all input rows
    candidates_all_lines = [x for x in range(1, len(chunk[0]))]
    for line in chunk:
        candidates_per_line = find_candidates(line)
        candidates_all_lines = [x for x in candidates_all_lines if x in candidates_per_line]
    assert len(candidates_all_lines) < 2
    return 0 if not candidates_all_lines else candidates_all_lines[0]


def find_horizontal_axis(chunk):
    return find_vertical_axis(transpose_list_of_strings(chunk))


def find_vertical_axis_v2(chunk):
    # find the one that is almost good enough, i.a. that would make a valid reflection axis for almost all lines in a chunk
    candidates_all_lines = {x: 0 for x in range(1, len(chunk[0]))}
    for line in chunk:
        candidates_per_line = find_candidates(line)
        for candidate in candidates_per_line:
            candidates_all_lines[candidate] += 1
    spicy_new_candidates = [x for x, y in candidates_all_lines.items() if y == len(chunk) - 1]
    assert len(spicy_new_candidates) < 2
    return 0 if not spicy_new_candidates else spicy_new_candidates[0]


def find_horizontal_axis_v2(chunk):
    return find_vertical_axis_v2(transpose_list_of_strings(chunk))


def split_into_chunks(problem):
    chunks = problem.split('\n\n')
    for i in range(len(chunks)):
        chunks[i] = chunks[i].split('\n')
    return chunks


def part_1(problem):
    return sum(find_vertical_axis(chunk) + find_horizontal_axis(chunk) * 100 for chunk in (split_into_chunks(problem)))


def part_2(problem):
    return sum(
        find_vertical_axis_v2(chunk) + find_horizontal_axis_v2(chunk) * 100 for chunk in split_into_chunks(problem))


if __name__ == '__main__':
    with open(input_file_name) as problem:
        data = problem.read()
        print(part_1(data))
        print(part_2(data))
