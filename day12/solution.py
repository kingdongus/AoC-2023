from functools import cache

from toolbox.toolbox import input_file_name


def solve(line, expansion_factor):
    springs, constraints = line.strip().split(' ')
    springs = '?'.join([springs] * expansion_factor) + '.'
    constraints = [int(n) for n in constraints.split(',')] * expansion_factor

    @cache
    def solve_rec(spring_index, constraint_index):
        if spring_index >= len(springs):
            return 1 if constraint_index == len(constraints) else 0

        result = 0
        # case 1: we have a ., or can place a ., so calculate the solution if we just move ahead by one
        if springs[spring_index] in '.?':
            result = solve_rec(spring_index + 1, constraint_index)

        # case 2: we have a # or ?, so let's check if we can find enough consecutive # or ? to consume the next constraint
        if constraint_index < len(constraints) and springs[spring_index] != '.':
            spring_index_after_next_constraint = spring_index + constraints[constraint_index]
            if ('.' not in springs[spring_index:spring_index_after_next_constraint]  # no . on the way
                    and '#' != springs[
                        spring_index_after_next_constraint]):  # we must not have another # right after the jump
                result += solve_rec(spring_index_after_next_constraint + 1, constraint_index + 1)

        return result

    return solve_rec(0, 0)


def part_1(problem):
    return sum((solve(line, 1) for line in problem))


def part_2(problem):
    return sum((solve(line, 5) for line in problem))


if __name__ == '__main__':
    with open(input_file_name) as problem:
        print(part_1(problem))
    with open(input_file_name) as problem:
        print(part_2(problem))
