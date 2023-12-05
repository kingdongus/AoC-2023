import re

from toolbox.toolbox import input_file_name


def overlaps(range1, range2):
    return not (range1[1] < range2[0] or range2[1] < range1[0])


def find_overlap(range1, range2):
    # Check if ranges overlap
    if not overlaps(range1, range2):
        return None  # Ranges do not overlap

    # Find the overlap range
    overlap_start = max(range1[0], range2[0])
    overlap_end = min(range1[1], range2[1])

    overlap_range = [overlap_start, overlap_end]
    return overlap_range


def is_range_contained(inner_range, outer_range):
    return inner_range[0] >= outer_range[0] and inner_range[1] <= outer_range[1]


def remove_overlap(range1, range2):
    # Check if ranges overlap
    if range1[1] < range2[0] or range2[1] < range1[0]:
        return []  # No overlap, return empty list

    # Find the overlap range
    overlap_start = max(range1[0], range2[0])
    overlap_end = min(range1[1], range2[1])

    # Remove overlapping parts from both ranges
    non_overlapping_range1 = [[range1[0], overlap_start - 1], [overlap_end + 1, range1[1]]]
    non_overlapping_range2 = [[range2[0], overlap_start - 1], [overlap_end + 1, range2[1]]]

    # Filter out empty ranges
    non_overlapping_range1 = [r for r in non_overlapping_range1 if r[0] < r[1]]
    non_overlapping_range2 = [r for r in non_overlapping_range2 if r[0] < r[1]]

    # Combine non-overlapping parts
    result = non_overlapping_range1 + non_overlapping_range2

    return result


class Rule:
    def __init__(self, source_start, delta, target_start):
        self.source_start = source_start
        self.target_start = target_start
        self.source_end = source_start + delta
        self.source_range = (self.source_start, self.source_end)

    def applies_to(self, n):
        return self.source_start <= n <= self.source_end

    def apply_to(self, n):
        return n - self.source_start + self.target_start

    def applies_to_range(self, start, end):
        # does it intersect?
        return overlaps(self.source_range, [start, end])

    def apply_to_range(self, start, end):
        # apply rule to intersecting part, return both post-rule intersection and unchanged interval
        input_range = [start, end]
        overlap = find_overlap(self.source_range, input_range)
        adjusted_new_range = [overlap[0] - self.source_start + self.target_start,
                              overlap[1] - self.source_start + self.target_start]

        out = []

        non_overlapping = remove_overlap(self.source_range, input_range)  # might contain 0 to 2 relevant elements
        for r in non_overlapping:
            if is_range_contained(r, input_range):
                out.append(r)
        return adjusted_new_range, out

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

    seed_ranges = [[seeds[x], seeds[x] + seeds[x + 1]] for x in range(0, len(seeds), 2)]
    current_gen = seed_ranges[::]
    for rule_set in rule_sets:
        next_gen = []
        current_leftovers = []
        while current_gen:
            next_seed_range = current_gen.pop()
            matched = False
            for rule in rule_set:
                if rule.applies_to_range(next_seed_range[0], next_seed_range[1]):
                    matched = True
                    updated, leftovers = rule.apply_to_range(next_seed_range[0], next_seed_range[1])
                    next_gen.append(updated)
                    for leftover in leftovers:
                        current_gen.append(leftover)
                    break
            if not matched:
                next_gen.append(next_seed_range)
        for leftover in current_leftovers:
            next_gen.append(leftover)
        current_gen = next_gen

    return min(x[0] for x in current_gen)


if __name__ == '__main__':
    # with open(input_file_name) as problem:
    #     print(part_1(problem))
    with open(input_file_name) as problem:
        print(part_2(problem))
