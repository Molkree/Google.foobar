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


from typing import Generator
from fractions import gcd


def all_pairs(lst):
    # type: (list[int]) -> Generator[list[tuple[int, int]], None, None]
    # Code by user shang on StackOverflow
    # https://stackoverflow.com/a/5360442/6026285
    if len(lst) < 2:
        yield []
        return
    if len(lst) % 2 == 1:
        # Handle odd length list
        for i in range(len(lst)):
            for result in all_pairs(lst[:i] + lst[i + 1 :]):
                yield result
    else:
        a = lst[0]
        for i in range(1, len(lst)):
            pair = (a, lst[i])
            for rest in all_pairs(lst[1:i] + lst[i + 1 :]):
                yield [pair] + rest


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


def solution(banana_list):
    # type: (list[int]) -> int
    max_busy_trainers = 0
    good_pairs = set()  # type: set[tuple[int, int]]
    bad_pairs = set()  # type: set[tuple[int, int]]
    for pairs in all_pairs(banana_list):
        busy_trainers = 0
        for num_1, num_2 in pairs:
            if check_pair(num_1, num_2, good_pairs, bad_pairs):
                busy_trainers += 2
        max_busy_trainers = max(max_busy_trainers, busy_trainers)
        if max_busy_trainers >= len(banana_list) - 1:
            break
    return len(banana_list) - max_busy_trainers


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
