# Distract the Trainers
# =====================

# The time for the mass escape has come, and you need to distract the bunny trainers so that the workers can make it out! Unfortunately for you, they're watching the bunnies closely. Fortunately, this means they haven't realized yet that the space station is about to explode due to the destruction of the LAMBCHOP doomsday device. Also fortunately, all that time you spent working as first a minion and then a henchman means that you know the trainers are fond of bananas. And gambling. And thumb wrestling.

# The bunny trainers, being bored, readily accept your suggestion to play the Banana Games.

# You will set up simultaneous thumb wrestling matches. In each match, two trainers will pair off to thumb wrestle. The trainer with fewer bananas will bet all their bananas, and the other trainer will match the bet. The winner will receive all of the bet bananas. You don't pair off trainers with the same number of bananas (you will see why, shortly). You know enough trainer psychology to know that the one who has more bananas always gets over-confident and loses. Once a match begins, the pair of trainers will continue to thumb wrestle and exchange bananas, until both of them have the same number of bananas. Once that happens, both of them will lose interest and go back to supervising the bunny workers, and you don't want THAT to happen!

# For example, if the two trainers that were paired started with 3 and 5 bananas, after the first round of thumb wrestling they will have 6 and 2 (the one with 3 bananas wins and gets 3 bananas from the loser). After the second round, they will have 4 and 4 (the one with 6 bananas loses 2 bananas). At that point they stop and get back to training bunnies.

# How is all this useful to distract the bunny trainers? Notice that if the trainers had started with 1 and 4 bananas, then they keep thumb wrestling! 1, 4 -> 2, 3 -> 4, 1 -> 3, 2 -> 1, 4 and so on.

# Now your plan is clear. You must pair up the trainers in such a way that the maximum number of trainers go into an infinite thumb wrestling loop!

# Write a function solution(banana_list) which, given a list of positive integers depicting the amount of bananas the each trainer starts with, returns the fewest possible number of bunny trainers that will be left to watch the workers. Element i of the list will be the number of bananas that trainer i (counting from 0) starts with.

# The number of trainers will be at least 1 and not more than 100, and the number of bananas each trainer starts with will be a positive integer no more than 1073741823 (i.e. 2^30 -1). Some of them stockpile a LOT of bananas.


# https://en.wikipedia.org/wiki/Blossom_algorithm
# https://github.com/RobertDurfee/Blossom


import copy
from fractions import gcd
from typing import Generator


def check_pair(num_1, num_2, good_pairs, bad_pairs):
    # type: (int, int, set[tuple[int, int]], set[tuple[int, int]]) -> bool
    if num_1 > num_2:
        num_1, num_2 = num_2, num_1
    pair = num_1, num_2
    if pair in good_pairs:
        return True
    elif pair in bad_pairs:
        return False
    n = (num_1 + num_2) // gcd(num_1, num_2)  # type: int
    is_not_2_power = (n & (n - 1)) != 0
    if is_not_2_power:
        good_pairs.add(pair)
    else:
        bad_pairs.add(pair)
    return is_not_2_power


class Graph:
    def __init__(self, edges):
        # type: (set[tuple[int, int]]) -> None
        self.neighbors = {}  # type: dict[int, set[int]]
        self.unmarked_neighbors = {}  # type: dict[int, set[int]]
        for i, j in edges:
            if i not in self.neighbors:
                self.neighbors[i] = set()
                self.unmarked_neighbors[i] = set()
            self.neighbors[i].add(j)
            self.unmarked_neighbors[i].add(j)
            if j not in self.neighbors:
                self.neighbors[j] = set()
                self.unmarked_neighbors[j] = set()
            self.neighbors[j].add(i)
            self.unmarked_neighbors[j].add(i)

    def get_vertices(self):
        # type: () -> list[int]
        return list(self.neighbors.keys())

    def unmark_all_edges(self):
        # type: () -> None
        self.unmarked_neighbors = copy.deepcopy(self.neighbors)

    def mark_edges(self, edges):
        # type: (set[tuple[int, int]]) -> None
        for edge in edges:
            self.mark_edge(edge)

    def mark_edge(self, edge):
        # type: (tuple[int, int]) -> None
        v, w = edge
        self.unmarked_neighbors[v].remove(w)
        if not self.unmarked_neighbors[v]:
            del self.unmarked_neighbors[v]
        self.unmarked_neighbors[w].remove(v)
        if not self.unmarked_neighbors[w]:
            del self.unmarked_neighbors[w]

    def get_unmarked_edge(self, vertex):
        # type: (int) -> tuple[int, int] | None
        if vertex in self.unmarked_neighbors:
            return vertex, next(iter(self.unmarked_neighbors[vertex]))

    def contract(self, blossom):
        # type: (Blossom) -> Graph
        graph_copy = copy.deepcopy(self)
        blossom_id = blossom.id
        graph_copy.neighbors[blossom_id] = set()
        for blossom_vertex in blossom.vertices:
            for neighbor in graph_copy.neighbors[blossom_vertex]:
                graph_copy.neighbors[neighbor].remove(blossom_vertex)
                if neighbor != blossom_id:
                    graph_copy.neighbors[blossom_id].add(neighbor)
                    graph_copy.neighbors[neighbor].add(blossom_id)
            del graph_copy.neighbors[blossom_vertex]
        if not graph_copy.neighbors[blossom_id]:
            del graph_copy.neighbors[blossom_id]
        graph_copy.unmark_all_edges()
        return graph_copy

    def lift_path(self, contracted_path, blossom):
        # type: (list[int], Blossom) -> list[int]
        if len(contracted_path) == 0:
            return contracted_path
        # left endpoint
        if contracted_path[0] == blossom.id:
            w = contracted_path[1]
            blossom_path = []  # type: list[int]
            for v in blossom.traverse_left():
                blossom_path.append(v)
                if (w in self.neighbors[v]) and (len(blossom_path) % 2 != 0):
                    return blossom_path + contracted_path[1:]
            blossom_path = []
            for v in blossom.traverse_right():
                blossom_path.append(v)
                if (w in self.neighbors[v]) and (len(blossom_path) % 2 != 0):
                    return blossom_path + contracted_path[1:]
        # right endpoint
        if contracted_path[-1] == blossom.id:
            u = contracted_path[-2]
            blossom_path = []
            for v in blossom.traverse_left():
                blossom_path.append(v)
                if (u in self.neighbors[v]) and (len(blossom_path) % 2 != 0):
                    return contracted_path[:-1] + list(reversed(blossom_path))
            blossom_path = []
            for v in blossom.traverse_right():
                blossom_path.append(v)
                if (u in self.neighbors[v]) and (len(blossom_path) % 2 != 0):
                    return contracted_path[:-1] + list(reversed(blossom_path))
        # somewhere inside the contracted path
        for i, v in enumerate(contracted_path):
            if v == blossom.id:
                u, w = contracted_path[i - 1], contracted_path[i + 1]
                if u in self.neighbors[blossom.root]:
                    blossom_path = []
                    for v in blossom.traverse_left():
                        blossom_path.append(v)
                        if (w in self.neighbors[v]) and (len(blossom_path) % 2 != 0):
                            contracted_path[i:i] = blossom_path
                            return contracted_path
                    blossom_path = []
                    for v in blossom.traverse_right():
                        blossom_path.append(v)
                        if (w in self.neighbors[v]) and (len(blossom_path) % 2 != 0):
                            contracted_path[i:i] = blossom_path
                            return contracted_path
                elif w in self.neighbors[blossom.root]:
                    blossom_path = []
                    for v in blossom.traverse_left():
                        blossom_path.append(v)
                        if (u in self.neighbors[v]) and (len(blossom_path) % 2 != 0):
                            contracted_path[i:i] = list(reversed(blossom_path))
                            return contracted_path
                    blossom_path = []
                    for v in blossom.traverse_right():
                        blossom_path.append(v)
                        if (u in self.neighbors[v]) and (len(blossom_path) % 2 != 0):
                            contracted_path[i:i] = list(reversed(blossom_path))
                            return contracted_path
        return contracted_path


class Matching:
    def __init__(self, vertices):
        # type: (list[int]) -> None
        self.edges = set()  # type: set[tuple[int, int]]
        self.exposed_vertices = set()  # type: set[int]
        self.neighbors = {}  # type: dict[int, set[int]]
        for vertice in vertices:
            self.neighbors[vertice] = set()
            self.exposed_vertices.add(vertice)

    def get_matched_vertex(self, vertex):
        # type: (int) -> int
        return next(iter(self.neighbors[vertex]))

    def contract(self, blossom):
        # type: (Blossom) -> Matching
        matching_copy = copy.deepcopy(self)
        blossom_id = blossom.id
        matching_copy.neighbors[blossom_id] = set()
        if blossom.root in matching_copy.exposed_vertices:
            matching_copy.exposed_vertices.add(blossom_id)
        for blossom_vertex in blossom.vertices:
            for blossom_neighbor in matching_copy.neighbors[blossom_vertex]:
                e = (
                    (blossom_vertex, blossom_neighbor)
                    if blossom_vertex < blossom_neighbor
                    else (blossom_neighbor, blossom_vertex)
                )
                matching_copy.edges.remove(e)
                matching_copy.neighbors[blossom_neighbor].remove(blossom_vertex)
                if blossom_neighbor != blossom_id:
                    new_edge = (
                        (blossom_id, blossom_neighbor)
                        if blossom_id < blossom_neighbor
                        else (blossom_neighbor, blossom_id)
                    )
                    matching_copy.edges.add(new_edge)
                    matching_copy.neighbors[blossom_id].add(blossom_neighbor)
                    matching_copy.neighbors[blossom_neighbor].add(blossom_id)
            del matching_copy.neighbors[blossom_vertex]
            matching_copy.exposed_vertices.discard(blossom_vertex)
        return matching_copy

    def augment(self, path):
        # type: (list[int]) -> Matching
        self.exposed_vertices.remove(path[0])
        self.exposed_vertices.remove(path[-1])
        for i in range(len(path) - 1):
            v, w = path[i], path[i + 1]
            edge = (v, w) if v < w else (w, v)
            if edge in self.edges:
                self.edges.remove(edge)
                self.neighbors[v].remove(w)
                self.neighbors[w].remove(v)
            else:
                self.edges.add(edge)
                self.neighbors[v].add(w)
                self.neighbors[w].add(v)
        return self


class Blossom:
    def __init__(self, root, vertices):
        # type: (int, list[int]) -> None
        self.root = root
        self.vertices = vertices
        self.id = -id(self)

    def traverse_right(self):
        # type: () -> Generator[int, None, None]
        for vertice in self.vertices:
            yield vertice

    def traverse_left(self):
        # type: () -> Generator[int, None, None]
        for vertice in [self.vertices[0]] + self.vertices[:0:-1]:
            yield vertice


class Forest:
    def __init__(self, roots):
        # type: (set[int]) -> None
        self.roots = {}  # type: dict[int, int]
        self.parents = {}  # type: dict[int, int]
        self.depths = {}  # type: dict[int, int]
        self.unmarked_even_vertices = set()  # type: set[int]
        for root in roots:
            self.roots[root] = root
            self.parents[root] = root
            self.depths[root] = 0
            self.unmarked_even_vertices.add(root)

    def get_unmarked_even_vertex(self):
        # type: () -> int | None
        return next(iter(self.unmarked_even_vertices), None)

    def add_edge(self, edge):
        # type: (tuple[int, int]) -> None
        v, w = edge
        self.roots[w] = self.roots[v]
        self.depths[w] = self.depths[v] + 1
        if self.depths[w] % 2 == 0:
            self.unmarked_even_vertices.add(w)
        self.parents[w] = v

    def get_bottom_up_path(self, vertex):
        # type: (int) -> list[int]
        path = []  # type: list[int]
        while self.parents[vertex] != vertex:
            path.append(vertex)
            vertex = self.parents[vertex]
        path.append(vertex)
        return path

    def get_blossom(self, v, w):
        # type: (int, int) -> Blossom
        w_path = self.get_bottom_up_path(w)
        blossom_vertices = [v]
        for u in w_path:
            if u == v:
                break
            else:
                blossom_vertices.append(u)
        return Blossom(v, blossom_vertices)

    def mark_vertex(self, vertex):
        # type: (int) -> None
        if self.depths[vertex] % 2 == 0:
            self.unmarked_even_vertices.remove(vertex)


def find_augmenting_path(graph, matching):
    # type: (Graph, Matching) -> list[int]
    graph.unmark_all_edges()
    graph.mark_edges(matching.edges)
    forest = Forest(matching.exposed_vertices)
    v = forest.get_unmarked_even_vertex()
    while v is not None:
        e = graph.get_unmarked_edge(v)
        while e:
            v, w = e
            if w not in forest.roots:
                forest.add_edge((v, w))
                x = matching.get_matched_vertex(w)
                forest.add_edge((w, x))
            else:
                if forest.depths[w] % 2 == 0:
                    if forest.roots[v] != forest.roots[w]:
                        return list(
                            reversed(forest.get_bottom_up_path(v))
                        ) + forest.get_bottom_up_path(w)
                    else:
                        blossom = forest.get_blossom(v, w)
                        contracted_graph = graph.contract(blossom)
                        contracted_matching = matching.contract(blossom)
                        contracted_path = find_augmenting_path(
                            contracted_graph, contracted_matching
                        )
                        return graph.lift_path(contracted_path, blossom)
            graph.mark_edge(e)
            e = graph.get_unmarked_edge(v)
        forest.mark_vertex(v)
        v = forest.get_unmarked_even_vertex()
    return []


def find_maximum_matching(graph, matching):
    # type: (Graph, Matching) -> Matching
    path = find_augmenting_path(graph, matching)
    if path:
        return find_maximum_matching(graph, matching.augment(path))
    return matching


def solution(banana_list):
    # type: (list[int]) -> int
    good_pairs = set()  # type: set[tuple[int, int]]
    bad_pairs = set()  # type: set[tuple[int, int]]
    edges = set()  # type: set[tuple[int, int]]
    for i, trainer in enumerate(banana_list):
        for j, other_trainer in enumerate(banana_list[i + 1 :], i + 1):
            if check_pair(trainer, other_trainer, good_pairs, bad_pairs):
                edges.add((i, j))
    graph = Graph(edges)
    matching = Matching(graph.get_vertices())
    busy_trainers_count = len(find_maximum_matching(graph, matching).edges) * 2
    return len(banana_list) - busy_trainers_count


good_pairs = set()  # type: set[tuple[int, int]]
bad_pairs = set()  # type: set[tuple[int, int]]
assert not check_pair(3, 5, good_pairs, bad_pairs)
assert not check_pair(1, 1, good_pairs, bad_pairs)
assert check_pair(1, 4, good_pairs, bad_pairs)
assert not check_pair(7, 1, good_pairs, bad_pairs)
assert check_pair(1, 13, good_pairs, bad_pairs)
assert check_pair(1, 19, good_pairs, bad_pairs)
assert check_pair(1, 21, good_pairs, bad_pairs)
assert check_pair(2, 3, good_pairs, bad_pairs)
assert not check_pair(2, 6, good_pairs, bad_pairs)
assert check_pair(3, 6, good_pairs, bad_pairs)
assert check_pair(3, 19, good_pairs, bad_pairs)
assert check_pair(3, 7, good_pairs, bad_pairs)
assert not check_pair(3, 13, good_pairs, bad_pairs)
assert check_pair(3, 19, good_pairs, bad_pairs)
assert not check_pair(3, 21, good_pairs, bad_pairs)
assert check_pair(7, 13, good_pairs, bad_pairs)
assert check_pair(7, 19, good_pairs, bad_pairs)
assert not check_pair(7, 21, good_pairs, bad_pairs)
assert not check_pair(13, 19, good_pairs, bad_pairs)
assert check_pair(13, 21, good_pairs, bad_pairs)
assert check_pair(19, 21, good_pairs, bad_pairs)
assert not check_pair(2 ** 30 - 1, 1, good_pairs, bad_pairs)

assert solution([3, 5]) == 2

assert solution([1, 4]) == 0

assert solution([1, 1]) == 2

assert solution([1, 7, 3, 21, 13, 19]) == 0

assert solution([1, 7, 21]) == 1

assert solution([3, 3, 2, 6, 6]) == 1
