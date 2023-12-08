import re

from toolbox.toolbox import input_file_name, lcmm

pattern = re.compile(r'(\w+) = \((\w+), (\w+)\)')


def extract_node(input_string):
    matches = pattern.findall(input_string)
    if matches:
        return matches[0][0], (matches[0][1], matches[0][2])
    else:
        return None


def parse_graph(problem):
    instructions = list(problem.readline().replace('\n', ''))
    problem.readline()  # skip empy line 🤡
    network = {}
    for line in problem.readlines():
        node, rl = extract_node(line)
        network[node] = rl
    return instructions, network


def find_path_for_node(current_node, instructions, network, end_condition):
    steps = 0
    # while not current_node == 'ZZZ':
    while not end_condition(current_node):
        instruction = instructions[steps % len(instructions)]
        next_targets = network[current_node]
        next_node = next_targets[0] if instruction == 'L' else next_targets[1]
        steps += 1
        current_node = next_node
    return steps


def all_end_with_z(strings):
    return len(strings) == len([s for s in strings if s.endswith('Z')])


def part_1(problem):
    instructions, network = parse_graph(problem)
    return find_path_for_node('AAA', instructions, network, lambda x: x == 'ZZZ')


def part_2(problem):
    instructions, network = parse_graph(problem)
    starting_nodes = [node for node in network.keys() if node.endswith('A')]
    individual_solutions = [find_path_for_node(node, instructions, network, lambda x: x.endswith('Z')) for node in
                            starting_nodes]
    return lcmm(*individual_solutions)


if __name__ == '__main__':
    with open(input_file_name) as problem:
        print(part_1(problem))
    with open(input_file_name) as problem:
        print(part_2(problem))
