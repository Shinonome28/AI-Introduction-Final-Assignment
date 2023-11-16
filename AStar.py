import heapq


def AStar(init, target, transformer, h, extra_data={}, max_steps=10000):
    states = [(h(0, target, init, **extra_data), 0, [init])]
    closed = []
    steps = 0
    while len(states) > 0:
        (_, depth, state) = heapq.heappop(states)
        steps += 1
        if steps > max_steps:
            return None
        if state[-1] in closed:
            continue
        closed.append(state[-1])
        if state[-1] == target:
            return state
        new_states = [
            (h(depth + 1, target, x, **extra_data), depth + 1, state + [x])
            for x in transformer(state[-1], **extra_data)
            if x not in closed
        ]
        for new_state in new_states:
            heapq.heappush(states, new_state)
    return None


# print(
#     AStar(
#         [0, 1, 5, 3, 7, 8, 6, 2, 4],
#         [1, 2, 3, 4, 5, 6, 7, 8, 0],
#         transformer.eight_digits,
#         transformer.eight_digits_h,
#     )
# )
