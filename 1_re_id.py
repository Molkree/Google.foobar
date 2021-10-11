# Re-ID
# =====
# There's some unrest in the minion ranks: minions with ID numbers like "1", "42", and other "good" numbers have been lording it over the poor minions who are stuck with more boring IDs. To quell the unrest, Commander Lambda has tasked you with reassigning everyone new random IDs based on a Completely Foolproof Scheme.

# Commander Lambda has concatenated the prime numbers in a single long string: "2357111317192329...". Now every minion must draw a number from a hat. That number is the starting index in that string of primes, and the minion's new ID number will be the next five digits in the string. So if a minion draws "3", their ID number will be "71113".

# Help the Commander assign these IDs by writing a function solution(n) which takes in the starting index n of Lambda's string of all primes, and returns the next five digits in the string. Commander Lambda has a lot of minions, so the value of n will always be between 0 and 10000.


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
