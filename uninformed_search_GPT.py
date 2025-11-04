import gymnasium as gym
import famnit_gym
import numpy as np
from collections import deque
import time

DIRS = {0: (-1, 0), 1: (0, 1), 2: (1, 0), 3: (0, -1)}

def get_player_crate_target_position(observation):
    crates, player, targets = [], None, []
    for i in range(len(observation)):
        for j in range(len(observation[i])):
            if observation[i][j] in [2, 4]:
                crates.append((i, j))
            elif observation[i][j] == 5:
                player = (i, j)
            elif observation[i][j] == 3:
                targets.append((i, j))
    return player, tuple(crates), tuple(targets)

def simulate(player, crates, action, map):
    dx, dy = DIRS[action]
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

def bfs_sokoban(player, crates, targets, map):
    queue = deque()
    visited = set()

    # Store states as (player_pos, crates_pos, path)
    queue.append((player, crates, []))
    visited.add((player, crates))

    while queue:
        player, crates, path = queue.popleft()

        if set(crates) == set(targets):
            return path

        for action in range(4):
            nxt = simulate(player, crates, action, map)
            if nxt is None:
                continue

            new_player, new_crates = nxt
            state = (new_player, new_crates)
            if state not in visited:
                visited.add(state)
                queue.append((new_player, new_crates, path + [action]))

    return None

# --- Main ---
env = gym.make("famnit_gym/Sokoban-v1", render_mode="human")
observation, info = env.reset()
player, crates, targets = get_player_crate_target_position(observation)
map = np.array(observation)

solution = bfs_sokoban(player, crates, targets, map)

if solution:
    print("Solution found:", solution)
    for a in solution:
        observation, reward, terminated, truncated, info = env.step(a)
        if terminated or truncated:
            break
else:
    print("No solution found!")

env.close()
