def BFS(init, target, transformer):
    states = [[init]]
    closed = []
    while len(states) > 0:
        if len(states) == 0:
            raise ValueError("Run out of states. Please check your transformer.")
        state = states[0]
        states.pop(0)
        closed.append(state[-1])
        if state[-1] == target:
            print(state)
            return True
        states += [
            state + [x]
            for x in transformer(state[-1])
            if x not in states and x not in closed
        ]
    return False


# BFS([0, 1, 5, 3, 7, 8, 6, 2, 4], [1, 2, 3, 4, 5, 6, 7, 8, 0], transformer.eight_digits)
