import sys

# part 1 legacy
number_strings = [str(x) for x in range(0,10)]
spicy_number_string = {'one':'1', 'two':'2', 'three':'3', 'four':'4', 'five':'5', 'six':'6', 'seven':'7', 'eight':'8', 'nine':'9'}

# part 2
def from_line(line):
    # only replace first and last match. lowest find, highest rfind
    lowest_text_match = min(spicy_number_string.items(), key=lambda x: line.find(x[0]) if x[0] in line else sys.maxsize)
    highest_text_match = max(spicy_number_string.items(), key=lambda x: line.rfind(x[0]))

    line = line.replace(lowest_text_match[0], lowest_text_match[1] + lowest_text_match[0]) # replace is not meant to exhaust the digit 🤡
    line = line.replace(highest_text_match[0], highest_text_match[1])

    numbers = [int(x) for x in line if x in number_strings]
    return int(str(numbers[0]) + str(numbers[-1]))

if __name__ == '__main__':
    # for i in [
    #     'two1nine',
    #     'eightwothree',
    #     'abcone2threexyz',
    #     'xtwone3four',
    #     '4nineeightseven2',
    #     'zoneight234',
    #     '7pqrstsixteen'
    # ]:
    #     print(from_line(i))
    with open('input.txt') as problem:
        print(sum([from_line(line) for line in problem.readlines()]))