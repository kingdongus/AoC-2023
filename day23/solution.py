from toolbox.Graph import UndirectedGraph
from toolbox.toolbox import input_file_name, read_file_into_2d_array, directions_2d_4, in_range, direction_east, \
    direction_west, direction_north, direction_south


def part_1(problem):
    # at each new field:
    # if there is one new direction*: move in that direction, increase path length by 1
    # a direction that was visited by an ancestor is not new
    # if there are multiple new directions: move in all of them, replace with generation of child streams
    # child stream id must be suffix to parent id, so we can identify the relationship later
    # on new field, replace longest match with max of visitors, including yours

    # *: new: I have not been there, none of my predecessors have been there, my siblings may have been there

    start, end = find_start_and_end(problem)
    memory = {(a, b): {} for a in range(len(problem)) for b in range(len(problem[0]))}

    work = [('0', start, 0)]

    def find_valid_next_locations(id, location):
        tile = problem[location[0]][location[1]]
        if tile in '<>^v':
            return handle_arrows(id, location, tile)

        locations = []
        # not arrows, all directions are possible
        for d in directions_2d_4:
            candidate_row = location[0] + d[0]
            candidate_col = location[1] + d[1]
            if not in_range(candidate_row, problem) or not in_range(candidate_col, problem[0]):
                continue
            if problem[candidate_row][candidate_col] == '#':
                continue
            visited_by_itself_or_ancestor = False
            if (candidate_row, candidate_col) in memory.keys():
                visited = memory[candidate_row, candidate_col]
                # visited by either this stream or an ancestor
                for v in visited.keys():
                    if id.startswith(v):
                        visited_by_itself_or_ancestor = True
                        continue
            if not visited_by_itself_or_ancestor:
                locations.append((candidate_row, candidate_col))
        return locations

    def handle_arrows(id, location, tile):
        locations = []
        if tile == '>':
            candidate_row = location[0] + direction_east[0]
            candidate_col = location[1] + direction_east[1]
        elif tile == '<':
            candidate_row = location[0] + direction_west[0]
            candidate_col = location[1] + direction_west[1]
        elif tile == '^':
            candidate_row = location[0] + direction_north[0]
            candidate_col = location[1] + direction_north[1]
        elif tile == 'v':
            candidate_row = location[0] + direction_south[0]
            candidate_col = location[1] + direction_south[1]
        visited_by_itself_or_ancestor = False
        if (candidate_row, candidate_col) in memory.keys():
            visited = memory[candidate_row, candidate_col]
            # visited by either this stream or an ancestor
            for v in visited.keys():
                if id.startswith(v):
                    visited_by_itself_or_ancestor = True
                    continue
        if not visited_by_itself_or_ancestor:
            locations.append((candidate_row, candidate_col))
        return locations

    # can we stop if we already saw a path with a higher step count?
    while work:
        stream_id, location, num_steps = work.pop()
        memory[location][stream_id] = num_steps
        next_locations = find_valid_next_locations(stream_id, location)
        if not next_locations:
            continue
        elif len(next_locations) == 1:
            work.append((stream_id, next_locations[0], num_steps + 1))
        else:
            for i in range(len(next_locations)):
                work.append((stream_id + str(i), next_locations[i], num_steps + 1))

    return max(memory[end].values())


def find_start_and_end(problem):
    start = (0, -1)
    for idx, x in enumerate(problem[0]):
        if x == '.':
            start = (0, idx)

    end = (len(problem) - 1, -1)
    for idx, x in enumerate(problem[-1]):
        if x == '.':
            end = (len(problem) - 1, idx)

    return start, end


def find_surrounding(location, grid):
    locations = []
    for d in directions_2d_4:
        candidate_row = location[0] + d[0]
        candidate_col = location[1] + d[1]
        if (not in_range(candidate_row, grid)
                or not in_range(candidate_col, grid[0])
                or grid[candidate_row][candidate_col] == '#'):
            continue
        locations.append((candidate_row, candidate_col))
    return locations


def part_2(problem):
    start, end = find_start_and_end(problem)
    intersections = {start, end}
    for i in range(len(problem)):
        for j in range(len(problem[0])):
            if problem[i][j] != '#' and len(find_surrounding((i, j), problem)) >= 3:
                intersections.add((i, j))

    graph = build_graph(intersections, problem)

    return graph.get_longest_path(start, end) - 1


def build_graph(intersections, problem):
    graph = UndirectedGraph()
    for intersection in intersections:
        dist = {intersection: 0}
        work = [intersection]
        while work:
            current = work.pop()
            for surrounding in find_surrounding(current, problem):
                if surrounding in dist.keys():
                    continue
                if surrounding in intersections:
                    graph.add_edge(intersection, surrounding, dist[current] + 1)
                    continue
                dist[surrounding] = dist[current] + 1
                work.append(surrounding)
    return graph


if __name__ == '__main__':
    problem = read_file_into_2d_array(input_file_name)
    print(part_1(problem))
    print(part_2(problem))
