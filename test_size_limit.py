from informed_search import astar, get_player_crate_target_position
from DFS import dfs
from BFS import bfs
from main_custom_size_goals import generate_custom_map as generate_custom_map_size_goals
from main_custom_size import generate_custom_map as generate_custom_map_size
import famnit_gym
import gymnasium as gym



map_astar = 1
while True:
    print("Testing A* with map size and goals:", map_astar)
    size = 5 + map_astar // 2        #velikost stpnevanje
    num_crates = 1 + map_astar // 2  # vsaki 2 mapi se doda nova škatla pa cilj
    custom_map = generate_custom_map_size_goals(size, num_crates)

    env = gym.make("famnit_gym/Sokoban-v1", render_mode=None, options={"map_template": custom_map})
    observation, info = env.reset()

    player, crates, targets = get_player_crate_target_position(observation)

    # A* del
    solution = astar(player, crates, targets, observation, timeout=60)
    if solution == -1:
        env.close()
        break
    env.close()
    map_astar += 1

map_dfs = 1
while True:
    print("DFS testing map with ", map_dfs, " crates")
    size = 5 + map_dfs // 2        #velikost stpnevanje
    num_crates = 1 + map_dfs // 2  # vsaki 2 mapi se doda nova škatla pa cilj
    custom_map = generate_custom_map_size_goals(size, num_crates)

    env = gym.make("famnit_gym/Sokoban-v1", render_mode=None, options={"map_template": custom_map})
    observation, info = env.reset()

    player, crates, targets = get_player_crate_target_position(observation)

    solution = dfs(player, crates, targets, observation, timeout=60)
    if solution == -1:
        env.close()
        break
    env.close()
    map_dfs += 1

map_bfs = 1
while True:
    print("BFS testing map with ", map_bfs, " crates")
    size = 5 + map_bfs // 2        #velikost stpnevanje
    num_crates = 1 + map_bfs // 2  # vsaki
    custom_map = generate_custom_map_size_goals(size, num_crates)

    env = gym.make("famnit_gym/Sokoban-v1", render_mode=None, options={"map_template": custom_map})
    observation, info = env.reset()

    player, crates, targets = get_player_crate_target_position(observation)

    solution = bfs(player, crates, targets, observation, timeout=60)
    if solution == -1:
        env.close()
        break   
    env.close()
    map_bfs += 1

print("Max map size for A*: ", 5 + map_astar // 2, "with ", map_astar, " crates")
print("Max map size for DFS: ", 5 + map_dfs // 2, "with ", map_dfs, " crates")
print("Max map size for BFS: ", 5 + map_bfs // 2, "with ", map_bfs, " crates")


map_astar_size = 1
while True:
    print("Testing A* with map size only:", map_astar_size)
    size = 5 + map_astar_size // 2  #velikost stpnevanje
    custom_map = generate_custom_map_size(size)

    env = gym.make('famnit_gym/Sokoban-v1', render_mode=None, options={'map_template': custom_map})
    observation, info = env.reset()

    player, crates, targets = get_player_crate_target_position(observation)

    # A* del
    solution = astar(player, crates, targets, observation, timeout=60)
    if solution == -1:
        env.close()
        break
    env.close()
    map_astar_size += 1


map_dfs_size = 1
while True:
    print("DFS testing map size only:", map_dfs_size)
    size = 5 + map_dfs_size // 2  #velikost stpnevanje
    custom_map = generate_custom_map_size(size)

    env = gym.make('famnit_gym/Sokoban-v1', render_mode=None, options={'map_template': custom_map})
    observation, info = env.reset()

    player, crates, targets = get_player_crate_target_position(observation)

    # A* del
    solution = dfs(player, crates, targets, observation, timeout=60)
    if solution == -1:
        env.close()
        break
    env.close()
    map_dfs_size += 1

map_bfs_size = 1
while True:
    print("BFS testing map size only:", map_bfs_size)
    size = 5 + map_bfs_size // 2  #velikost stpnevanje
    custom_map = generate_custom_map_size(size)

    env = gym.make('famnit_gym/Sokoban-v1', render_mode=None, options={'map_template': custom_map})
    observation, info = env.reset()

    player, crates, targets = get_player_crate_target_position(observation)
    solution = bfs(player, crates, targets, observation, timeout=60)
    if solution == -1:
        env.close()
        break
    env.close()
    map_bfs_size += 1

print("Max map size for A* (size only): ", 5 + map_astar_size // 2)
print("Max map size for DFS (size only): ", 5 + map_dfs_size // 2)
print("Max map size for BFS (size only): ", 5 + map_bfs_size // 2)
