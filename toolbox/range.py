class Range:
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def overlaps_with(self, other):
        return not (self.start > other.end or self.end < other.start)

    # todo override __and__ and make that work
    def logical_and(self, other):
        if not self.overlaps_with(other):
            return None
        return Range(max(self.start, other.start), min(self.end, other.end))

    # if ranges overlap, combine into one
    # if not, return disjunct list of ranges
    # todo override __or__ and make that work
    def logical_or(self, other):
        if not self.overlaps_with(other):
            return [Range(self.start, self.end), Range(other.start, other.end)]
        return [Range(min(self.start, other.start), max(self.end, other.end))]

    def logical_xor(self, other):
        # no overlap
        if not self.overlaps_with(other):
            return [Range(self.start, self.end), Range(other.start, other.end)]
        # full overlap - nothing left
        if self == other:
            return []

        # either start or end is equal
        if self.start == other.start:
            return [Range(min(self.end, other.end), max(self.end, other.end))]

        if self.end == other.end:
            return [Range(min(self.start, other.start), max(self.start, other.start))]

        overlap = self.logical_and(other)
        return [Range(min(self.start, other.start), overlap.start - 1),
                Range(overlap.end + 1, max(self.end, other.end))]

    # like logical_xor, but also return the overlapping interval
    def split_by(self, other):
        # no overlap
        if not self.overlaps_with(other):
            return [Range(self.start, self.end), Range(other.start, other.end)]
        # full overlap
        if self == other:
            return [Range(self.start, self.end)]
        # partial overlap

        # either start or end is equal
        if self.start == other.start:
            return [Range(self.start, min(self.end, other.end)), Range(min(self.end, other.end) + 1, self.end)]

        if self.end == other.end:
            return [Range(min(self.start, other.start), max(self.start, other.start)),
                    Range(max(self.start, other.start) + 1, self.end)]

        xored = self.logical_xor(other)
        xored.append(self.logical_and(other))
        return sorted(xored, key=lambda x: x.start)

    def __eq__(self, other):
        return self.start == other.start and self.end == other.end

    def __contains__(self, other):
        return other.start >= self.start and other.end <= self.end

    def __repr__(self):
        return f'[{self.start} - {self.end}]'

    def __str__(self):
        return self.__repr__()


if __name__ == '__main__':
    print(Range(0, 1).overlaps_with(Range(1, 2)))  # true
    print(Range(0, 1).overlaps_with(Range(2, 3)))  # false
    print(Range(0, 1).overlaps_with(Range(0, 1)))  # true
    print(Range(0, 1).overlaps_with(Range(1, 0)))  # true
    print(Range(0, 1).overlaps_with(Range(-1, 2)))  # true
    print(Range(-1, 2).overlaps_with(Range(0, 1)))  # true

    print(Range(1, 3).logical_and(Range(1, 3)))  # [1,3]
    print(Range(1, 3).logical_and(Range(4, 5)))  # None
    print(Range(1, 3).logical_and(Range(3, 4)))  # [3,3]
    print(Range(1, 1).logical_and(Range(2, 2)))  # None
    print(Range(1, 5).logical_and(Range(4, 10)))  # [4,5]
    print(Range(1, 10).logical_and(Range(5, 20)))  # [5,10]
    print(Range(5, 20).logical_and(Range(1, 10)))  # [5,10]

    print(Range(1, 2) in Range(0, 3))  # true
    print(Range(1, 2) in Range(2, 3))  # false
    print(Range(1, 2) in Range(1, 2))  # true
    print(Range(1, 2) in Range(0, 1))  # false
    print(Range(0, 3) in Range(1, 2))  # false
    print(Range(2, 3) in Range(1, 2))  # false

    print(Range(1, 2).logical_or(Range(2, 3)))  # [[1,3]]
    print(Range(1, 2).logical_or(Range(3, 4)))  # [[1,2], [3,4]]
    print(Range(1, 3).logical_or(Range(2, 4)))  # [1,4]

    print('>>>>>>>>>>>> logical xor')
    print(Range(1, 10).logical_xor(Range(1, 10)))  # None
    print(Range(1, 10).logical_xor(Range(2, 9)))  # [[1,1], [10,10]]
    print(Range(1, 10).logical_xor(Range(3, 8)))  # [[1,2],[9,10]]
    print(Range(1, 10).logical_xor(Range(5, 10)))  # [[1,4]]
    print(Range(1, 10).logical_xor(Range(5, 12)))  # [[1,4],[11,12]]]
    print(Range(1, 10).logical_xor(Range(5, 5)))  # [[1,4],[6,10]]]
    print(Range(1, 10).logical_xor(Range(2, 2)))  # [[1,1],[3,10]]]
    print(Range(1, 2).logical_xor(Range(3, 4)))  # [[1,2],[3,4]]]

    print('>>>>>>>>>>>> split by')
    print(Range(1, 10).split_by(Range(1, 10)))  # [1,10]
    print(Range(1, 10).split_by(Range(2, 9)))  # [[1,1],[2,9], [10,10]]
    print(Range(1, 10).split_by(Range(3, 8)))  # [[1,2],[3,8],[9,10]]
    print(Range(1, 10).split_by(Range(5, 10)))  # [[1,4], [5,10]]
    print(Range(1, 10).split_by(Range(1, 5)))  # [[1,4], [5,10]]
    print(Range(1, 10).split_by(Range(5, 12)))  # [[1,4],[5,10],[11,12]]]
    print(Range(1, 10).split_by(Range(5, 5)))  # [[1,4],[5,5],[6,10]]]
    print(Range(1, 10).split_by(Range(2, 2)))  # [[1,1],[2,2],[3,10]]]
    print(Range(1, 2).logical_xor(Range(3, 4)))  # [[1,2],[3,4]]]
