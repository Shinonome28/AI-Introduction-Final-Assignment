def eight_digits(state):
    def swap(l, i, j):
        r = l[:]
        t = r[i]
        r[i] = r[j]
        r[j] = t
        return r

    for i in range(0, len(state)):
        if i - 3 >= 0 and state[i - 3] == 0:
            yield swap(state, i - 3, i)
        elif i + 3 <= 8 and state[i + 3] == 0:
            yield swap(state, i + 3, i)
        elif i - 1 >= 0 and state[i - 1] == 0 and ((i - 1) % 3 == i % 3 - 1):
            yield swap(state, i - 1, i)
        elif i + 1 <= 8 and state[i + 1] == 0 and ((i + 1) % 3 == i % 3 + 1):
            yield swap(state, i + 1, i)


def eight_digits_h(depth, target, state):
    c = 0
    for i in range(0, len(target)):
        if state[i] != target[i]:
            t = target.index(state[i])
            c += abs(t // 3 - i // 3) + abs(t % 3 - i % 3)
    return c + depth
