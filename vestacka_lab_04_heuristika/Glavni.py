from queue import PriorityQueue


def heuristic(state, goal):
    return sum(1 for (s, g) in zip(state, goal) if s == g)


def get_next_states(state):
    colors = ['W', 'Y', 'R', 'G', 'B']
    next_states = []
    for i in range(len(state)):
        for color in colors:
            if state[i] != color:
                new_state = state[:]
                new_state[i] = color
                next_states.append(new_state)
    return next_states


def best_first_search(initial_state, goal_state):
    priority_queue = PriorityQueue()
    priority_queue.put((-heuristic(initial_state, goal_state), initial_state, []))
    """sa minusom je zbog priority queue-a, on uzima najmanji broj"""
    visited = set()
    passed = 0

    while not priority_queue.empty():
        _, current_state, path = priority_queue.get()
        passed += 1
        if tuple(current_state) in visited:
            continue
        visited.add(tuple(current_state))
        if current_state == goal_state:
            print("prodjeno puta: ", passed)
            return path + [current_state]

        for next_state in get_next_states(current_state):
            if tuple(next_state) not in visited:
                next_score = heuristic(next_state, goal_state)
                priority_queue.put((-next_score, next_state, path + [current_state]))
    return None

"""pocetno stanje"""
initial_state = ['G', 'Y', 'R', 'G']
"""ciljno stanje"""
goal_state = ['Y', 'Y', 'B', 'R']

path = best_first_search(initial_state, goal_state)

if path:
    print("Put do cilja:")
    for step in path:
        print(step)
else:
    print(":(")
