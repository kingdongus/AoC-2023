import re
from collections import namedtuple

from toolbox.range import Range
from toolbox.toolbox import input_file_name

Part = namedtuple('Part', ['x', 'm', 'a', 's'])


class PartInterval:
    def __init__(self):
        self.x = Range(1, 4000)
        self.m = Range(1, 4000)
        self.a = Range(1, 4000)
        self.s = Range(1, 4000)

    def clone(self):
        t = PartInterval()
        t.x = self.x.clone()
        t.m = self.m.clone()
        t.a = self.a.clone()
        t.s = self.s.clone()
        return t

    def split_at_x(self, at):
        split_at = self.x.split_at(at)
        t1 = self.clone()
        t1.x = split_at[0]
        t2 = self.clone()
        t2.x = split_at[1]
        return t1, t2

    def split_at_m(self, at):
        split_at = self.m.split_at(at)
        t1 = self.clone()
        t1.m = split_at[0]
        t2 = self.clone()
        t2.m = split_at[1]
        return t1, t2

    def split_at_a(self, at):
        split_at = self.a.split_at(at)
        t1 = self.clone()
        t1.a = split_at[0]
        t2 = self.clone()
        t2.a = split_at[1]
        return t1, t2

    def split_at_s(self, at):
        split_at = self.s.split_at(at)
        t1 = self.clone()
        t1.s = split_at[0]
        t2 = self.clone()
        t2.s = split_at[1]
        return t1, t2

    def __repr__(self):
        return f'PartInterval x:{self.x}, m{self.m}, a:{self.a}, s:{self.s}'


class Rule:
    def __init__(self, outcome, condition=None):
        self.outcome = outcome
        self.condition = condition
        if condition:
            self.operator = ">" if ">" in self.condition else "<"
            self.target = condition.split(self.operator)[0]
            self.value = int(condition.split(self.operator)[1])

    def apply_to_part(self, part):
        if not self.condition:
            return True
        return eval('part.' + self.condition)

    def apply_to_interval(self, interval: PartInterval):
        if not self.condition:
            return [(interval, self.outcome)]
        if self.target == 'x' and self.operator == '<' and interval.x.start < self.value < interval.x.end:
            t1, t2 = interval.split_at_x(self.value - 1)
            return [(t1, self.outcome), (t2,)]
        if self.target == 'x' and self.operator == '>' and interval.x.start < self.value < interval.x.end:
            t1, t2 = interval.split_at_x(self.value)
            return [(t1,), (t2, self.outcome)]
        if self.target == 'm' and self.operator == '<' and interval.m.start < self.value < interval.m.end:
            t1, t2 = interval.split_at_m(self.value - 1)
            return [(t1, self.outcome), (t2,)]
        if self.target == 'm' and self.operator == '>' and interval.m.start < self.value < interval.m.end:
            t1, t2 = interval.split_at_m(self.value)
            return [(t1,), (t2, self.outcome)]
        if self.target == 'a' and self.operator == '<' and interval.a.start < self.value < interval.a.end:
            t1, t2 = interval.split_at_a(self.value - 1)
            return [(t1, self.outcome), (t2,)]
        if self.target == 'a' and self.operator == '>' and interval.a.start < self.value < interval.a.end:
            t1, t2 = interval.split_at_a(self.value)
            return [(t1,), (t2, self.outcome)]
        if self.target == 's' and self.operator == '<' and interval.s.start < self.value < interval.s.end:
            t1, t2 = interval.split_at_s(self.value - 1)
            return [(t1, self.outcome), (t2,)]
        if self.target == 's' and self.operator == '>' and interval.s.start < self.value < interval.s.end:
            t1, t2 = interval.split_at_s(self.value)
            return [(t1,), (t2, self.outcome)]
        return None

    def __repr__(self):
        return f'Rule (outcome: {self.outcome}, condition: {self.condition})'


class Workflow:

    def __init__(self, name, rules):
        self.rules = rules
        self.name = name

    def apply_to_part(self, part):
        for rule in self.rules:
            if rule.apply_to_part(part):
                return rule.outcome
        return None

    def apply_to_interval(self, interval: PartInterval):
        ret = []
        remainder = interval
        for r in self.rules:
            result = r.apply_to_interval(remainder)
            if not result:
                continue
            if len(result) == 1:
                ret.append(result[0])
                continue
            a, b = result[0], result[1]
            remainder = a[0] if len(a) == 1 else b[0]
            ret.append(a if len(a) == 2 else b)

        return ret

    @staticmethod
    def from_line(line):
        name = line.split('{')[0]
        meat = extract_rule_content(line)
        rules = []
        for r in meat[0].split(','):
            if ':' in r:
                condition, outcome = r.split(':')
                rules.append(Rule(outcome, condition))
            else:
                rules.append(Rule(r))
        return Workflow(name, rules)

    def __repr__(self):
        return f'Workflow {self.name}: {self.rules}'


def extract_rule_content(input_line):
    pattern = re.compile(r'.*{(.*)}')

    matches = pattern.findall(input_line)

    if matches:
        return list(matches)
    else:
        return None


def extract_numeric_values(input_line):
    pattern = re.compile(r'\b(\d+)\b')

    matches = pattern.findall(input_line)

    if matches:
        return list(map(int, matches))
    else:
        return None


def parse_input(problem):
    workflows, parts = problem.read().split('\n\n')
    parsed_workflows = [Workflow.from_line(workflow) for workflow in workflows.split('\n')]
    parsed_parts = [Part(*(extract_numeric_values(part))) for part in parts.split('\n')]
    return parsed_workflows, parsed_parts


def part_1(problem):
    workflows, parts = parse_input(problem)

    workflow_index = {x.name: x for x in workflows}

    accepted = set()
    rejected = set()

    for part in parts:
        outcome = workflow_index['in'].apply_to_part(part)
        while outcome:
            if outcome == 'A':
                accepted.add(part)
                break
            elif outcome == 'R':
                rejected.add(part)
                break
            else:
                outcome = workflow_index[outcome].apply_to_part(part)

    return sum(x.x + x.m + x.a + x.s for x in accepted)


def part_2(problem):
    workflows, _ = parse_input(problem)
    workflow_index = {x.name: x for x in workflows}

    work = [(PartInterval(), 'in')]

    accept = []
    reject = []

    while work:
        interval, workflow_name = work.pop()
        if workflow_name == 'A':
            accept.append(interval)
            continue
        if workflow_name == 'R':
            reject.append(interval)
            continue
        workflow = workflow_index[workflow_name]
        result = workflow.apply_to_interval(interval)
        for r in result:
            work.append(r)

    return sum((len(a.x) * len(a.m) * len(a.a) * len(a.s) for a in accept))


if __name__ == '__main__':
    with open(input_file_name) as problem:
        print(part_1(problem))
    with open(input_file_name) as problem:
        print(part_2(problem))
