import gymnasium as gym
import famnit_gym

DIRS = {
    0: (-1, 0),  # Up
    1: (0, 1),   # Right
    2: (1, 0),   # Down
    3: (0, -1)   # Left
}

def get_player_crate_target_position(observation):
    crate_cord = []
    player_cord = None
    target_cord = []
    for i in range(len(observation)):
        for j in range(len(observation[i])):
            if observation[i][j] in [2, 4]:
                crate_cord.append((i, j))
            elif observation[i][j] == 5:
                player_cord = (i, j)
            elif observation[i][j] == 3:
                target_cord.append((i, j))
    return player_cord, tuple(crate_cord), tuple(target_cord)

def simulate(player, crates, action, map):
    (dx, dy) = DIRS[action]
    px, py = player
    npx, npy = px + dx, py + dy

    crates = set(crates)

    # Player hits wall
    if map[npx][npy] == 1:
        return None

    # Player pushes crate
    if (npx, npy) in crates:
        ncx, ncy = npx + dx, npy + dy
        if map[ncx][ncy] == 1 or (ncx, ncy) in crates:
            return None
        crates.remove((npx, npy))
        crates.add((ncx, ncy))

    return (npx, npy), tuple(crates)

def dfs(player, crates, targets, map, max_depth=5000):
    """Uninformed search: Depth-First Search"""
    stack = [(player, crates, [])]
    visited = set()

    while stack:
        player, crates, path = stack.pop()
        state = (player, crates)

        if state in visited:
            continue
        visited.add(state)

        # Goal check
        if set(crates) == set(targets):
            return path

        # Optional depth limit (to avoid infinite recursion)
        if len(path) >= max_depth:
            continue

        # Explore moves (order affects exploration pattern)
        for move in range(4):
            nxt = simulate(player, crates, move, map)
            if nxt is None:
                continue
            new_player, new_crates = nxt
            new_state = (new_player, new_crates)

            if new_state not in visited:
                # Push next state to stack (LIFO)
                stack.append((new_player, new_crates, path + [move]))

    return None

# --- Main Execution ---
env = gym.make("famnit_gym/Sokoban-v1", render_mode="human")
observation, info = env.reset()

player, crates, targets = get_player_crate_target_position(observation)

solution = dfs(player, crates, targets, observation)

if solution is None:
    print("No solution found!")
else:
    print("Solution:", solution)
    for a in solution:
        observation, reward, terminated, truncated, info = env.step(a)
        if terminated or truncated:
            break
    env.close()

