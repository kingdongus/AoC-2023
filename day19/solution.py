import re
from collections import namedtuple

from toolbox.toolbox import input_file_name

Part = namedtuple('Part', ['x', 'm', 'a', 's'])


class Rule:
    def __init__(self, outcome, cond=None):
        self.outcome = outcome
        if cond and 'x' in cond:
            self.condition = cond.replace('x', 'part.x')
        elif cond and 'm' in cond:
            self.condition = cond.replace('m', 'part.m')
        elif cond and 'a' in cond:
            self.condition = cond.replace('a', 'part.a')
        elif cond and 's' in cond:
            self.condition = cond.replace('s', 'part.s')
        elif not cond:
            self.condition = None

    def applies_to(self, part):
        if not self.condition:
            return True
        return eval(self.condition)

    def __repr__(self):
        return f'Rule (outcome: {self.outcome}, condition: {self.condition})'


class Workflow:

    def __init__(self, name, rules):
        self.rules = rules
        self.name = name

    def apply(self, part):
        for rule in self.rules:
            if rule.applies_to(part):
                return rule.outcome
        return None

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
        outcome = workflow_index['in'].apply(part)
        while outcome:
            if outcome == 'A':
                accepted.add(part)
                break
            elif outcome == 'R':
                rejected.add(part)
                break
            else:
                outcome = workflow_index[outcome].apply(part)

    return sum(x.x + x.m + x.a + x.s for x in accepted)


def part_2(problem):
    pass


if __name__ == '__main__':
    with open(input_file_name) as problem:
        print(part_1(problem))
    with open(input_file_name) as problem:
        print(part_2(problem))
