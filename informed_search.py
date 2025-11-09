import heapq


DIRS = {
    0: (-1, 0), # Up
    1: (0, 1),  # Right
    2: (1, 0),  # Down
    3: (0, -1)  # Left
}


def get_player_crate_target_position(observation):
    crate_cord = []
    player_cord = None
    target_cord = []
    for i in range(len(observation)):
        for j in range(len(observation[i])):
            if observation[i][j] in [2,4]:
                crate_cord.append((i, j))
            elif observation[i][j] == 5:
                player_cord = (i, j)
            elif observation[i][j] == 3:
                target_cord.append((i, j))
    return player_cord, tuple(crate_cord), tuple(target_cord)


def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def heuristic(crates, targets):
    total = 0
    for crate in crates:
        total += min(manhattan(crate, target) for target in targets)
    return total

def simulate(player, crates, action, map):
    (dx, dy) = DIRS[action]
    px, py = player
    npx, npy = px + dx, py + dy

    crates = set(crates)

    if map[npx][npy] == 1:
        return None

    if (npx, npy) in crates:
        ncx, ncy = npx + dx, npy + dy

        if map[ncx][ncy] == 1 or (ncx, ncy) in crates:
            return None

        crates.remove((npx, npy))
        crates.add((ncx, ncy))

    return ((npx, npy), tuple(crates))


def astar(player, crates, targets, map):

    heap = []
    visited = set()

    g = 0
    h = heuristic(crates, targets)

    heapq.heappush(heap, (g + h, g, player, crates, []))


    while heap:
        f, g, player, crates, path = heapq.heappop(heap)

        state = (player, crates)
        if state in visited:
            continue
        visited.add(state)

        if set(crates) == set(targets):
            return path

        for move in range(4):
            nxt = simulate(player, crates, move, map)
            if nxt is None:
                continue

            new_player, new_crates = nxt
            new_state = (new_player, new_crates)

            if new_state not in visited:
                g2 = g + 1
                h2 = heuristic(new_crates, targets)
                heapq.heappush(heap, (g2 + h2, g2, new_player, new_crates, path + [move]))

    return None