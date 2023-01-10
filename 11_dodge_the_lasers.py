# Dodge the Lasers!
# =================

# Oh no! You've managed to escape Commander Lambda's collapsing space station in an
# escape pod with the rescued bunny workers - but Commander Lambda isnt about to let
# you get away that easily. Lambda sent an elite fighter pilot squadron after you --
# and they've opened fire!

# Fortunately, you know something important about the ships trying to shoot you down.
# Back when you were still Lambda's assistant, the Commander asked you to help program
# the aiming mechanisms for the starfighters. They undergo rigorous testing procedures,
# but you were still able to slip in a subtle bug. The software works as a time step
# simulation: if it is tracking a target that is accelerating away at 45 degrees, the
# software will consider the targets acceleration to be equal to the square root of 2,
# adding the calculated result to the targets end velocity at each timestep. However,
# thanks to your bug, instead of storing the result with proper precision, it will be
# truncated to an integer before adding the new velocity to your current position.
# This means that instead of having your correct position, the targeting software will
# erringly report your position as sum(i=1..n, floor(i*sqrt(2))) - not far enough off
# to fail Commander Lambdas testing, but enough that it might just save your life.

# If you can quickly calculate the target of the starfighters' laser beams to know how
# far off they'll be, you can trick them into shooting an asteroid, releasing dust, and
# concealing the rest of your escape.  Write a function solution(str_n) which, given
# the string representation of an integer n, returns the sum of (floor(1*sqrt(2)) +
# floor(2*sqrt(2)) + ... + floor(n*sqrt(2))) as a string. That is, for every number i
# in the range 1 to n, it adds up all of the integer portions of i*sqrt(2).

# For example, if str_n was "5", the solution would be calculated as
# floor(1*sqrt(2)) +
# floor(2*sqrt(2)) +
# floor(3*sqrt(2)) +
# floor(4*sqrt(2)) +
# floor(5*sqrt(2))
# = 1+2+4+5+7 = 19
# so the function would return "19".

# str_n will be a positive integer between 1 and 10^100, inclusive. Since n can be very
# large (up to 101 digits!), using just sqrt(2) and a loop won't work. Sometimes, it's
# easier to take a step back and concentrate not on what you have in front of you, but
# on what you don't.

# https://en.wikipedia.org/wiki/Beatty_sequence
# https://math.stackexchange.com/questions/2052179/how-to-find-sum-i-1n-left-lfloor-i-sqrt2-right-rfloor-a001951-a-beatty-s
# https://towardsdatascience.com/dodge-the-lasers-fantastic-question-from-googles-hiring-challenge-72363d95fec
from decimal import Decimal, localcontext


def rec(n):
    # type: (Decimal) -> Decimal
    if n < 2:
        return n
    r = Decimal(2).sqrt()
    s = Decimal(2) + Decimal(2).sqrt()  # type: Decimal
    beatty_rn = int(n * r)
    beatty_rn_s = int(beatty_rn / s)
    return (
        beatty_rn * (beatty_rn + 1) / 2
        - beatty_rn_s * (beatty_rn_s + 1)
        - rec(beatty_rn_s)
    )


def solution(str_n):
    # type: (str) -> str
    with localcontext() as ctx:
        ctx.prec = 101
        n = Decimal(str_n)
        return str(rec(n))


assert solution("5") == "19"
assert solution("1" * 15) == "8729713347982073754917440345"
assert (
    solution("1" * 100)
    == "872971334798206820247956002598579060845476466282066711837456628389341036087720394352091070572618254830224283883999278509942557409036661858897798926520732750054962505827308960636251324550880747783752"
)
assert (
    solution("2" * 100)
    == "3491885339192827280991824010394316243381905865128266847349826513557364144350881577408364282290473018860659844010335948704560536069815449024844667509473960803909030033606481995759406575550707071533251"
)
assert (
    solution("9" * 100)
    == "70710678118654752440084436210484903928483593768847403658833986899536623923105351942519376716382078624679624499680139607237798181744046467783846697970256425687262443342712887327254803273119967464820709"
)
