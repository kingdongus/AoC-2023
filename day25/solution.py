from toolbox.Graph import UndirectedGraph
from toolbox.toolbox import input_file_name


def part_1(problem):
    g = UndirectedGraph()
    for line in problem:
        f, t = line.split(':')
        t = t.split(' ')
        for x in t:
            if not x:
                continue
            g.add_edge(f, x.strip(), 1)

    # HOW TO
    # 1. visualize graph
    # 2. look closely
    # 3. find edges
    # generic graph partitioning might be NP hard, ain't nobody got time for that

    g.visualize()

    for e in [('szh', 'vqj'), ('jbx', 'sml'), ('zhb', 'vxr')]:
        g.remove_edge(e[0], e[1])

    size_1 = g.count_size_of_group_from('szh')
    size_2 = g.count_size_of_group_from('vqj')

    return size_1 * size_2


def part_2(problem):
    return 'done 🤡👍'


if __name__ == '__main__':
    with open(input_file_name) as problem:
        print(part_1(problem))  # 2322768 too high
    with open(input_file_name) as problem:
        print(part_2(problem))
