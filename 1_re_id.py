def gen_primes():
    # Code by David Eppstein, UC Irvine, 28 Feb 2002
    # http://code.activestate.com/recipes/117119/
    composite2primes = {}
    candidate = 2
    while True:
        if candidate not in composite2primes:
            yield candidate
            composite2primes[candidate * candidate] = [candidate]
        else:
            for prime in composite2primes[candidate]:
                composite2primes.setdefault(candidate + prime, []).append(prime)
            del composite2primes[candidate]
        candidate += 1


def gen_id_string(str_length):
    result = ""
    for prime in gen_primes():
        result += str(prime)
        if len(result) >= str_length:
            break
    return result


def solution(i):
    max_minion_number = 100000
    id_length = 5
    id_string = gen_id_string(max_minion_number + id_length)
    return id_string[i:i + id_length]


assert "23571" == solution(0)
assert "35711" == solution(1)
assert "71113" == solution(3)
