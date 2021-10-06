def geometric_sequence(seed=1, factor=2):
    while True:
        yield seed
        seed *= factor


def fibonacci():
    yield 1
    prev_prev = 1
    yield 1
    prev = 1
    while True:
        yield prev_prev + prev
        prev_prev, prev = prev, prev_prev + prev


def count_seq_less_than_sum(gen, sum):
    count = 0
    for num in gen():
        if sum - num < 0:
            break
        sum -= num
        count += 1
    return count


def solution(total_lambs):
    max_henchmen = count_seq_less_than_sum(fibonacci, total_lambs)
    min_henchmen = count_seq_less_than_sum(geometric_sequence, total_lambs)
    return max_henchmen - min_henchmen


assert 1 == solution(10)
assert 3 == solution(143)
