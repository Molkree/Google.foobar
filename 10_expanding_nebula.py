# Expanding Nebula
# ================

# You've escaped Commander Lambda's exploding space station along with numerous escape
# pods full of bunnies. But -- oh no! -- one of the escape pods has flown into a nearby
# nebula, causing you to lose track of it. You start monitoring the nebula, but
# unfortunately, just a moment too late to find where the pod went. However, you do
# find that the gas of the steadily expanding nebula follows a simple pattern, meaning
# that you should be able to determine the previous state of the gas and narrow down
# where you might find the pod.

# From the scans of the nebula, you have found that it is very flat and distributed in
# distinct patches, so you can model it as a 2D grid. You find that the current
# existence of gas in a cell of the grid is determined exactly by its 4 nearby cells,
# specifically, (1) that cell, (2) the cell below it, (3) the cell to the right of it,
# and (4) the cell below and to the right of it. If, in the current state, exactly 1 of
# those 4 cells in the 2x2 block has gas, then it will also have gas in the next state.
# Otherwise, the cell will be empty in the next state.

# For example, let's say the previous state of the grid (p) was:
# .O..
# ..O.
# ...O
# O...

# To see how this grid will change to become the current grid (c) over the next time
# step, consider the 2x2 blocks of cells around each cell.  Of the 2x2 block of
# [p[0][0], p[0][1], p[1][0], p[1][1]], only p[0][1] has gas in it, which means this
# 2x2 block would become cell c[0][0] with gas in the next time step:
# .O -> O
# ..

# Likewise, in the next 2x2 block to the right consisting of [p[0][1], p[0][2],
# p[1][1], p[1][2]], two of the containing cells have gas, so in the next state of the
# grid, c[0][1] will NOT have gas:
# O. -> .
# .O

# Following this pattern to its conclusion, from the previous state p, the current
# state of the grid c will be:
# O.O
# .O.
# O.O

# Note that the resulting output will have 1 fewer row and column, since the bottom and
# rightmost cells do not have a cell below and to the right of them, respectively.

# Write a function solution(g) where g is an array of array of bools saying whether
# there is gas in each cell (the current scan of the nebula), and return an int with
# the number of possible previous states that could have resulted in that grid after 1
# time step.  For instance, if the function were given the current state c above, it
# would deduce that the possible previous states were p (given above) as well as its
# horizontal and vertical reflections, and would return 4. The width of the grid will
# be between 3 and 50 inclusive, and the height of the grid will be between 3 and 9
# inclusive.  The solution will always be less than one billion (10^9).


from collections import defaultdict
from itertools import product


def solution(g):
    # type: (list[list[bool]]) -> int

    height = len(g)

    # Because max height is just 9, we can generate all column combinations
    # It's height + 1 because we need previous grid state
    cell_combinations = product((True, False), repeat=height + 1)

    # Then we generate all 2 column combinations
    preimages = product(cell_combinations, repeat=2)

    # From these 2 column combinations we can calculate the next state of the (thin, 2 cell) grid
    mapping = defaultdict(
        list
    )  # type: defaultdict[tuple[bool, ...], list[tuple[tuple[bool, ...], ...]]]
    for preimage in preimages:
        image = []  # type: list[bool]
        for i in range(height):
            if sum(preimage[0][i : i + 2]) + sum(preimage[1][i : i + 2]) == 1:
                image.append(True)
            else:
                image.append(False)
        mapping[tuple(image)].append(preimage)

    # We transpose original grid to work with columns, not rows
    transposed = list(zip(*g))

    # Then for each column (now row) we check what could be the previous state
    # and for each step from column to column we make sure that their previous states overlap
    candidates = mapping[transposed[0]]
    for row in transposed[1:]:
        next_candidates = mapping[row]
        filtered_candidates = []  # type: list[tuple[tuple[bool, ...], ...]]
        for next_candidate, candidate in product(next_candidates, candidates):
            if candidate[1] == next_candidate[0]:
                filtered_candidates.append(next_candidate)
        candidates = filtered_candidates
    return len(candidates)


grid = [[True, False, True], [False, True, False], [True, False, True]]
assert solution(grid) == 4

grid = [
    [True, False, True, False, False, True, True, True],
    [True, False, True, False, False, False, True, False],
    [True, True, True, False, False, False, True, False],
    [True, False, True, False, False, False, True, False],
    [True, False, True, False, False, True, True, True],
]
assert solution(grid) == 254

grid = [
    [True, True, False, True, False, True, False, True, True, False],
    [True, True, False, False, False, False, True, True, True, False],
    [True, True, False, False, False, False, False, False, False, True],
    [False, True, False, False, False, False, True, True, False, False],
]
assert solution(grid) == 11567
