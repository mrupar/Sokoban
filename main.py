import gymnasium as gym
import famnit_gym
import time
import os
import csv

from informed_search import astar
from DFS import dfs
from BFS import bfs

result_dict = {}

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

csv_file = "results.csv"

with open(csv_file, mode="w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["map_id", "algorithm", "time", "length", "map_string"])


for i in range(1000):
    print(i)
    env = gym.make("famnit_gym/Sokoban-v1", options={"map":i})
    observation, info = env.reset()

    player, crates, targets = get_player_crate_target_position(observation)

    # A*
    start = time.time()
    print("Running A* search...")
    a_star_solution = astar(player, crates, targets, observation)
    a_star_time = time.time() - start
    a_star_length = len(a_star_solution) if a_star_solution is not None else 0

    # DFS
    start = time.time()
    print("Running DFS search...")
    dfs_solution = dfs(player, crates, targets, observation)
    dfs_time = time.time() - start
    dfs_length = len(dfs_solution) if dfs_solution is not None else 0

    # BFS
    start = time.time()
    print("Running BFS search...")
    bfs_solution = bfs(player, crates, targets, observation)
    bfs_time = time.time() - start
    bfs_length = len(bfs_solution) if bfs_solution is not None else 0

    env.close()

    map_string = f'[{";".join([" ".join(map(str, row)) for row in observation])}]'
    with open(csv_file, mode="a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([i, "A*", a_star_time, a_star_length, map_string])
        writer.writerow([i, "DFS", dfs_time, dfs_length, map_string])
        writer.writerow([i, "BFS", bfs_time, bfs_length, map_string])
