from collections import defaultdict

import matplotlib.pyplot as plt
import networkx as nx


class Node:
    def __init__(self):
        self.incoming = set()
        self.outgoing = set()
        self.distances = {}


class UndirectedGraph:
    def __init__(self):
        self.edges = defaultdict(set)
        self.distance = {}

    def add_edge(self, node1, node2, distance):
        self.edges[node1].add(node2)
        self.edges[node2].add(node1)
        self.distance[node1, node2] = distance
        self.distance[node2, node1] = distance

    def remove_edge(self, node1, node2):
        self.edges[node1].remove(node2)
        self.edges[node2].remove(node1)
        self.distance[node1, node2] = -1
        self.distance[node2, node1] = -1

    def count_size_of_group_from(self, node):
        if not self.edges[node]:
            return 0

        count = 1
        seen = {node}
        work = self.edges[node].copy()

        while work:
            n = work.pop()
            if n in seen:
                continue
            count += 1
            seen.add(n)
            for x in self.edges[n]:
                work.add(x)

        return count

    def get_outgoing(self, node):
        return self.edges[node]

    def get_longest_path(self, start, end, visited=set()):
        if start == end:
            return 1
        longest = None
        for outgoing in self.get_outgoing(start):
            if outgoing in visited:
                continue
            partial = self.get_longest_path(outgoing, end, visited | {start})
            if not partial:
                continue
            dist = self.distance[start, outgoing]
            if not longest:
                longest = partial + dist
            else:
                longest = max(longest, partial + dist)
        result = longest
        return result

    def visualize(self):
        G = nx.Graph()
        flat_edges = []
        for k, v in self.edges.items():
            for t in v:
                flat_edges.append([k, t])
        G.add_edges_from(flat_edges)
        nx.draw_networkx(G)
        plt.show()
