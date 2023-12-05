import re

from toolbox.range import Range
from toolbox.toolbox import input_file_name


class Rule:
    def __init__(self, source_start, delta, target_start):
        self.source_start = source_start
        self.target_start = target_start
        self.source_end = source_start + delta
        self.source_range = Range(source_start, source_start + delta)

    def applies_to(self, n):
        return n in self.source_range

    def apply_to(self, n):
        return n - self.source_start + self.target_start

    def applies_to_range(self, range):
        # does it intersect?
        return self.source_range.overlaps_with(range)

    def apply_to_range(self, range):
        # apply rule to intersecting part, return both post-rule intersection and unchanged interval(s)
        split = self.source_range.logical_xor(range)
        overlap = self.source_range.logical_and(range)
        unchanged = [r for r in split if r != overlap and r in range]
        adjusted_new_range = Range(overlap.start - self.source_start + self.target_start,
                                   overlap.end - self.source_start + self.target_start)

        return adjusted_new_range, unchanged

    def __repr__(self):
        return f'[from: {self.source_start} to: {self.source_end}, target_start: {self.target_start}]'

    def __str__(self):
        return self.__repr__()


def part_1(problem):
    grouped_rules, seeds = extract_seeds_and_rules(problem.read())

    new_seeds = []
    for seed in seeds:
        for group in grouped_rules:
            # in each group find at most one rule that applies
            for rule in group:
                if rule.applies_to(seed):
                    seed = rule.apply_to(seed)
                    break
        new_seeds.append(seed)

    return min(new_seeds)


def extract_seeds_and_rules(data):
    blocks = re.split(r'\n\w+-to-\w+ map:\n', data)
    seeds = []
    grouped = []
    for block in blocks:
        if block:
            lines = block.split('\n')
            lines = [line.strip() for line in lines if line.strip()]
            rules = []
            for line in lines:
                numbers = re.findall(r'\d+', line)
                numbers = list(map(int, numbers))
                if len(numbers) != 3:
                    seeds = numbers
                else:
                    rules.append(Rule(numbers[1], numbers[2], numbers[0]))
            if rules:
                grouped.append(rules)
    return grouped, seeds


def part_2(problem):
    data = problem.read()

    rule_sets, seeds = extract_seeds_and_rules(data)

    seed_ranges = [Range(seeds[x], seeds[x] + seeds[x + 1]) for x in range(0, len(seeds), 2)]

    for rule_set in rule_sets:
        next_gen = []
        while seed_ranges:
            next_seed_range = seed_ranges.pop()
            matched = False
            for rule in rule_set:
                if rule.applies_to_range(next_seed_range):
                    matched = True
                    updated, leftovers = rule.apply_to_range(next_seed_range)
                    next_gen.append(updated)
                    for leftover in leftovers:
                        seed_ranges.append(leftover)
                    break
            if not matched:
                next_gen.append(next_seed_range)
        seed_ranges = next_gen

    return min(x.start for x in seed_ranges)


if __name__ == '__main__':
    with open(input_file_name) as problem:
        print(part_1(problem))
    with open(input_file_name) as problem:
        print(part_2(problem))
