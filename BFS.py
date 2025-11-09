DIRS = {        
    0: (-1, 0),  # gor
    1: (0, 1),   # desno
    2: (1, 0),   # dol
    3: (0, -1)   # levo
}


# -----------------------------------------------------------
#import gymnasium as gym
#import famnit_gym
#import numpy as np



# ta array je za delat mapo
# 1 je zid, 5 je player, 2 je skatla in 3 je cilj
#custom_map = np.array([
#    [1, 1, 1, 1, 1],
#    [1, 5, 0, 0, 1],
#    [1, 0, 2, 0, 1],
#    [1, 0, 0, 3, 1],
#    [1, 1, 1, 1, 1],
#], dtype=np.uint8)

#env = gym.make('famnit_gym/Sokoban-v1', render_mode='human', options={'map_template': custom_map})
#observation, info = env.reset()

#def get_player_crate_target_position(observation):
#    crate_cord = []
#    player_cord = None
#    target_cord = []
#    for i in range(len(observation)):
#        for j in range(len(observation[i])):
#            if observation[i][j] in [2, 4]:
#                crate_cord.append((i, j))
#            elif observation[i][j] == 5:
#                player_cord = (i, j)
#            elif observation[i][j] == 3:
#                target_cord.append((i, j))
#    return player_cord, tuple(crate_cord), tuple(target_cord)

# -----------------------------------------------------------



def simulate(player, crates, action, map):
    (dx, dy) = DIRS[action]
    px, py = player
    npx, npy = px + dx, py + dy

    crates = set(crates)

    # prever a se zabijamo v steno
    if map[npx][npy] == 1:
        return None

    # prever a porivamo skatlo
    if (npx, npy) in crates:
        ncx, ncy = npx + dx, npy + dy

        # prever a se skatla da premaknt
        if map[ncx][ncy] == 1 or (ncx, ncy) in crates:
            return None

        crates.remove((npx, npy))
        crates.add((ncx, ncy))

    return (npx, npy), tuple(crates)

def bfs(player, crates, targets, map):
    #BFS main
    queue = [(player, crates, [])]
    visited = set()

    while queue:
        player, crates, path = queue.pop(0)
        state = (player, tuple(sorted(crates)))

        if state in visited:
            continue
        visited.add(state)

        # prever gol
        if set(crates) == set(targets):
            return path

        # razisc moznosti
        for move in range(4):
            nxt = simulate(player, crates, move, map)
            if nxt is None:
                continue
            new_player, new_crates = nxt
            new_state = (new_player, new_crates)

            if new_state not in visited:
                queue.append((new_player, new_crates, path + [move]))

    return None
