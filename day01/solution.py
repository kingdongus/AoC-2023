import sys

# part 1 legacy
number_strings = [str(x) for x in range(1, 10)]
spicy_number_strings = dict(
    zip(['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine'], number_strings))


# part 2
def from_line(line):
    # only replace first and last match. lowest find, highest rfind
    lowest_text_match = min(spicy_number_strings.items(),
                            key=lambda x: line.find(x[0]) if x[0] in line else sys.maxsize)
    # replace is not meant to exhaust the digit 🤡
    # if we don't do this magic, oneight would evaluate to 11 when it should be 18
    line = line.replace(lowest_text_match[0], lowest_text_match[1] + lowest_text_match[0])

    highest_text_match = max(spicy_number_strings.items(), key=lambda x: line.rfind(x[0]))
    line = line.replace(highest_text_match[0], highest_text_match[1])

    numbers = [int(x) for x in line if x in number_strings]
    return int(str(numbers[0]) + str(numbers[-1]))


if __name__ == '__main__':
    with open('input.txt') as problem:
        print(sum([from_line(line) for line in problem.readlines()]))
