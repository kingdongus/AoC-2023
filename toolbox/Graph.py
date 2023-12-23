from collections import defaultdict


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
