# Prepare the Bunnies' Escape
# ===========================

# You're awfully close to destroying the LAMBCHOP doomsday device and freeing Commander Lambda's bunny workers, but once they're free of the work duties the bunnies are going to need to escape Lambda's space station via the escape pods as quickly as possible. Unfortunately, the halls of the space station are a maze of corridors and dead ends that will be a deathtrap for the escaping bunnies. Fortunately, Commander Lambda has put you in charge of a remodeling project that will give you the opportunity to make things a little easier for the bunnies. Unfortunately (again), you can't just remove all obstacles between the bunnies and the escape pods - at most you can remove one wall per escape pod path, both to maintain structural integrity of the station and to avoid arousing Commander Lambda's suspicions.

# You have maps of parts of the space station, each starting at a work area exit and ending at the door to an escape pod. The map is represented as a matrix of 0s and 1s, where 0s are passable space and 1s are impassable walls. The door out of the station is at the top left (0,0) and the door into an escape pod is at the bottom right (w-1,h-1).

# Write a function solution(map) that generates the length of the shortest path from the station door to the escape pod, where you are allowed to remove one wall as part of your remodeling plans. The path length is the total number of nodes you pass through, counting both the entrance and exit nodes. The starting and ending positions are always passable (0). The map will always be solvable, though you may or may not need to remove a wall. The height and width of the map can be from 2 to 20. Moves can only be made in cardinal directions; no diagonal moves are allowed.


from collections import deque


def solution(map):
    def neighbors(map, node, visited, did_demolish):
        def is_possible_neighbor(i, j, map, visited):
            height = len(map)
            width = len(map[0])
            return (
                0 <= i <= height - 1 and 0 <= j <= width - 1 and (i, j) not in visited
            )

        i, j = node
        i -= 1
        if is_possible_neighbor(i, j, map, visited):
            if map[i][j] == 0:
                yield (i, j), did_demolish
            elif not did_demolish:
                yield (i, j), True
        i, j = node
        i += 1
        if is_possible_neighbor(i, j, map, visited):
            if map[i][j] == 0:
                yield (i, j), did_demolish
            elif not did_demolish:
                yield (i, j), True
        i, j = node
        j -= 1
        if is_possible_neighbor(i, j, map, visited):
            if map[i][j] == 0:
                yield (i, j), did_demolish
            elif not did_demolish:
                yield (i, j), True
        i, j = node
        j += 1
        if is_possible_neighbor(i, j, map, visited):
            if map[i][j] == 0:
                yield (i, j), did_demolish
            elif not did_demolish:
                yield (i, j), True

    def bfs(map, node, previous, queue):
        did_demolish = False
        queue.append((node, did_demolish))
        while queue:
            next_node, did_demolish = queue.popleft()
            for neighbor, did_demolish in neighbors(
                map, next_node, previous, did_demolish
            ):
                if neighbor not in previous:
                    previous[neighbor] = next_node
                    queue.append((neighbor, did_demolish))
                    if neighbor == (height - 1, width - 1):
                        break

    height = len(map)
    width = len(map[0])
    previous = {(0, 0): None}
    bfs(map, (0, 0), previous, deque())
    length = 1
    node = (height - 1, width - 1)
    while node != (0, 0):
        node = previous[node]
        length += 1
    return length


map = [[0, 0], [0, 0]]
# print(solution(map))
assert 3 == solution(map)

# 7
map = [[0, 1, 1, 0], [0, 0, 0, 1], [1, 1, 0, 0], [1, 1, 1, 0]]
# print(solution(map))
assert 7 == solution(map)

# 21
map = [
    [0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 1],
    [0, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0],
]
assert 11 == solution(map)
