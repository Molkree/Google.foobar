# Escape Pods
# ===========

# You've blown up the LAMBCHOP doomsday device and relieved the bunnies of their work
# duries -- and now you need to escape from the space station as quickly and as orderly
# as possible! The bunnies have all gathered in various locations throughout the
# station, and need to make their way towards the seemingly endless amount of escape
# pods positioned in other parts of the station. You need to get the numerous bunnies
# through the various rooms to the escape pods. Unfortunately, the corridors between
# the rooms can only fit so many bunnies at a time. What's more, many of the corridors
# were resized to accommodate the LAMBCHOP, so they vary in how many bunnies can move
# through them at a time.

# Given the starting room numbers of the groups of bunnies, the room numbers of the
# escape pods, and how many bunnies can fit through at a time in each direction of
# every corridor in between, figure out how many bunnies can safely make it to the
# escape pods at a time at peak.

# Write a function solution(entrances, exits, path) that takes an array of integers
# denoting where the groups of gathered bunnies are, an array of integers denoting
# where the escape pods are located, and an array of an array of integers of the
# corridors, returning the total number of bunnies that can get through at each time
# step as an int. The entrances and exits are disjoint and thus will never overlap. The
# path element path[A][B] = C describes that the corridor going from A to B can fit C
# bunnies at each time step.  There are at most 50 rooms connected by the corridors and
# at most 2000000 bunnies that will fit at a time.

# For example, if you have:
# entrances = [0, 1]
# exits = [4, 5]
# path = [
#   [0, 0, 4, 6, 0, 0],  # Room 0: Bunnies
#   [0, 0, 5, 2, 0, 0],  # Room 1: Bunnies
#   [0, 0, 0, 0, 4, 4],  # Room 2: Intermediate room
#   [0, 0, 0, 0, 6, 6],  # Room 3: Intermediate room
#   [0, 0, 0, 0, 0, 0],  # Room 4: Escape pods
#   [0, 0, 0, 0, 0, 0],  # Room 5: Escape pods
# ]

# Then in each time step, the following might happen:
# 0 sends 4/4 bunnies to 2 and 6/6 bunnies to 3
# 1 sends 4/5 bunnies to 2 and 2/2 bunnies to 3
# 2 sends 4/4 bunnies to 4 and 4/4 bunnies to 5
# 3 sends 4/6 bunnies to 4 and 4/6 bunnies to 5

# So, in total, 16 bunnies could make it to the escape pods at 4 and 5 at each time
# step. (Note that in this example, room 3 could have sent any variation of 8 bunnies
# to 4 and 5, such as 2/6 and 6/6, but the final solution remains the same.)

# https://en.wikipedia.org/wiki/Edmonds%E2%80%93Karp_algorithm
# https://github.com/anxiaonong/Maxflow-Algorithms/blob/master/Edmonds-Karp%20Algorithm.py
MAX_FLOW = 2000000


def bfs(capacities, flows, source, sink):
    # type: (list[list[int]], list[list[int]], int, int) -> list[tuple[int, int]] | None
    queue = [source]
    paths = {source: []}  # type: dict[int, list[tuple[int, int]]]
    if source == sink:
        return paths[source]
    while queue:
        u = queue.pop(0)
        for v in range(len(capacities)):
            if (capacities[u][v] - flows[u][v] > 0) and v not in paths:
                paths[v] = paths[u] + [(u, v)]
                if v == sink:
                    return paths[v]
                queue.append(v)
    return None


def edmonds_karp(capacities, source, sink):
    # type: (list[list[int]], int, int) -> int
    node_count = len(capacities)
    flows = [[0] * node_count for _ in range(node_count)]
    path = bfs(capacities, flows, source, sink)
    while path is not None:
        flow = min(capacities[u][v] - flows[u][v] for u, v in path)
        for u, v in path:
            flows[u][v] += flow
            flows[v][u] -= flow
        path = bfs(capacities, flows, source, sink)
    return sum(flows[source][i] for i in range(node_count))


def solution(entrances, exits, path):
    # type: (list[int], list[int], list[list[int]]) -> int
    wrapped_matrix = (
        [[0] * (len(path) + 2)]
        + [[0] + row + [0] for row in path]
        + [[0] * (len(path) + 2)]
    )
    for entrance in entrances:
        wrapped_matrix[0][entrance + 1] = MAX_FLOW
        wrapped_matrix[entrance + 1][0] = MAX_FLOW
    for exit in exits:
        wrapped_matrix[exit + 1][-1] = MAX_FLOW
        wrapped_matrix[-1][exit + 1] = MAX_FLOW
    return edmonds_karp(wrapped_matrix, 0, len(wrapped_matrix) - 1)


entrances = [0, 1]
exits = [4, 5]
path = [
    [0, 0, 4, 6, 0, 0],  # Room 0: Bunnies
    [0, 0, 5, 2, 0, 0],  # Room 1: Bunnies
    [0, 0, 0, 0, 4, 4],  # Room 2: Intermediate room
    [0, 0, 0, 0, 6, 6],  # Room 3: Intermediate room
    [0, 0, 0, 0, 0, 0],  # Room 4: Escape pods
    [0, 0, 0, 0, 0, 0],  # Room 5: Escape pods
]
assert solution(entrances, exits, path) == 16

entrances = [0]
exits = [3]
path = [
    [0, 7, 0, 0],  # Room 0: Bunnies
    [0, 0, 6, 0],  # Room 1: Intermediate room
    [0, 0, 0, 8],  # Room 2: Intermediate room
    [9, 0, 0, 0],  # Room 3: Escape pods
]
assert solution(entrances, exits, path) == 6
