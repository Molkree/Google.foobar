# Disorderly Escape
# =================

# Oh no! You've managed to free the bunny workers and escape Commander Lambdas exploding space station, but
# Lambda's team of elite starfighters has flanked your ship. If you dont jump to hyperspace, and fast, youll
# be shot out of the sky!

# Problem is, to avoid detection by galactic law enforcement, Commander Lambda planted the space station in
# the middle of a quasar quantum flux field. In order to make the jump to hyperspace, you need to know the
# configuration of celestial bodies in the quadrant you plan to jump through. In order to do *that*, you need
# to figure out how many configurations each quadrant could possibly have, so that you can pick the optimal
# quadrant through which youll make your jump.

# There's something important to note about quasar quantum flux fields' configurations: when drawn on a star
# grid, configurations are considered equivalent by grouping rather than by order. That is, for a given set
# of configurations, if you exchange the position of any two columns or any two rows some number of times,
# youll find that all of those configurations are equivalent in that way -- in grouping, rather than order.

# Write a function solution(w, h, s) that takes 3 integers and returns the number of unique, non-equivalent
# configurations that can be found on a star grid w blocks wide and h blocks tall where each celestial body
# has s possible states. Equivalency is defined as above: any two star grids with each celestial body in the
# same state where the actual order of the rows and columns do not matter (and can thus be freely swapped
# around). Star grid standardization means that the width and height of the grid will always be between 1 and
# 12, inclusive. And while there are a variety of celestial bodies in each grid, the number of states of those
# bodies is between 2 and 20, inclusive. The solution can be over 20 digits long, so return it as a decimal
# string.  The intermediate values can also be large, so you will likely need to use at least 64-bit integers.

# For example, consider w=2, h=2, s=2. We have a 2x2 grid where each celestial body is either in state 0 (for
# instance, silent) or state 1 (for instance, noisy).  We can examine which grids are equivalent by swapping
# rows and columns.

# 00
# 00
# In the above configuration, all celestial bodies are "silent" - that is, they have a state of 0 - so any
# swap of row or column would keep it in the same state.

# 00 00 01 10
# 01 10 00 00
# 1 celestial body is emitting noise - that is, has a state of 1 - so swapping rows and columns can put it in
# any of the 4 positions.  All four of the above configurations are equivalent.

# 00 11
# 11 00
# 2 celestial bodies are emitting noise side-by-side.  Swapping columns leaves them unchanged, and swapping
# rows simply moves them between the top and bottom.  In both, the *groupings* are the same: one row with two
# bodies in state 0, one row with two bodies in state 1, and two columns with one of each state.

# 01 10
# 01 10
# 2 noisy celestial bodies adjacent vertically. This is symmetric to the side-by-side case, but it is
# different because there's no way to transpose the grid.

# 01 10
# 10 01
# 2 noisy celestial bodies diagonally.  Both have 2 rows and 2 columns that have one of each state, so they
# are equivalent to each other.

# 01 10 11 11
# 11 11 01 10
# 3 noisy celestial bodies, similar to the case where only one of four is noisy.

# 11
# 11
# 4 noisy celestial bodies.

# There are 7 distinct, non-equivalent grids in total, so solution(2, 2, 2) would return 7.


# https://math.stackexchange.com/questions/2056708/
# Essentially Kody Puebla's solution with some minor modifications.


from fractions import Fraction, gcd
from itertools import product
from math import factorial


def solution(w, h, s):
    # type: (int, int, int) -> str

    grid_count = 0
    # generate cycle indices for the set of rows and set of columns
    cycle_index_rows = cycle_index(h)
    cycle_index_cols = cycle_index(w)
    # combine every possible pair of row and column permutations
    for (coeff_row, cycle_row), (coeff_col, cycle_col) in product(
        cycle_index_rows, cycle_index_cols
    ):
        coeff = coeff_row * coeff_col
        cycle = combine(cycle_row, cycle_col)
        # substitue each variable for state s
        value = 1
        for power in cycle:
            value *= s**power
        # multiply by the coefficient and add to the total
        grid_count += coeff * value
    return str(grid_count)


def cycle_index(n):
    # type: (int) -> list[tuple[Fraction, list[tuple[int, int]]]]
    """
    Combine sets of variables with their coefficients to generate a complete cycle index.
    """
    return [(coeff(term), term) for term in gen_vars(n, n)]


def coeff(term):
    # type: (list[tuple[int, int]]) -> Fraction
    """
    Calculate the coefficient of a term based on values associated with its variable(s).

    This is based off part of the general formula for finding the cycle index of a symmetric group.
    """
    value = 1
    for x, y in term:
        value *= factorial(y) * x**y
    return Fraction(1, value)


def gen_vars(n, limit):
    # type: (int, int) -> list[list[tuple[int, int]]]
    """
    Generate the solution set to the problem: what are all combinations of numbers <= n that sum to n?

    This corresponds to the set of variables in each term of the cycle index of symmetric group S_n.
    """
    solution_set = []  # type: list[list[tuple[int, int]]]
    if not n:
        return solution_set
    for x in range(limit, 1, -1):
        for y in range(n // x, 0, -1):
            # use recursion on the remainder across all values smaller than x
            recurse = gen_vars(n - x * y, x - 1)
            # if recursion comes up empty, add the value by itself to the solution set
            if not recurse:
                solution_set.append([(x, y)])
            # otherwise, append the current value to each solution and add that to the solution set
            for solution in recurse:
                solution_set.append([(x, y)] + solution)
    solution_set.append([(1, n)])
    return solution_set


def combine(term_a, term_b):
    # type: (list[tuple[int, int]], list[tuple[int, int]]) -> list[int]
    """
    Combine two terms of a cycle index of the form [ ( int:{length}, int:{frequency} ):{cycle}, ... ].
    """
    combined = []  # type: list[int]
    for (length_a, frequency_a), (length_b, frequency_b) in product(term_a, term_b):
        lcm = length_a * length_b / gcd(length_a, length_b)  # type: int
        combined.append(length_a * frequency_a * length_b * frequency_b // lcm)
    return combined


assert solution(2, 2, 2) == "7"
assert solution(2, 3, 2) == "13"

# OEIS A058001: https://oeis.org/A058001
assert solution(3, 3, 1) == "1"
assert solution(3, 3, 2) == "36"
assert solution(3, 3, 3) == "738"

# OEIS A058002: https://oeis.org/A058002
assert solution(4, 4, 1) == "1"
assert solution(4, 4, 2) == "317"
assert solution(4, 4, 3) == "90492"

# OEIS A058003: https://oeis.org/A058003
assert solution(5, 5, 1) == "1"
assert solution(5, 5, 2) == "5624"
assert solution(5, 5, 3) == "64796982"
