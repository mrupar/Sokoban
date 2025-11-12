import gymnasium as gym
import famnit_gym
import numpy as np
import time
import csv
import random

from informed_search import astar
from DFS import dfs
from BFS import bfs

#Modificirana verzija main_custom_size.py sam dodal sm da se ob vsakem vecanju poveca stevilo skatel da se pogleda kk to vpliva na cajt

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

# Generacija map
def generate_custom_map(size, num_crates):
    """

    - 1 = zid
    - 0 = prazno
    - 5 = player
    - 2 = škatla
    - 3 = cilj
    """
        #stena okoli in prazna notranjost
    m = np.ones((size, size), dtype=np.uint8)
    m[1:-1, 1:-1] = 0

    # player je vedno levo zgori
    m[1, 1] = 5

    free_spaces = [(i, j) for i in range(2, size - 2) for j in range(2, size - 2)]
    random.shuffle(free_spaces)

    # Vecanje st skatel, golov in velikosti
    for _ in range(num_crates):
        if len(free_spaces) < 2:
            break
        crate_pos = free_spaces.pop()
        target_pos = free_spaces.pop()
        m[crate_pos] = 2
        m[target_pos] = 3

    return m


if __name__ == "__main__":
    csv_file = "results_custom_map_size_goals.csv"
    
    with open(csv_file, mode="w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["map_id", "map_size", "num_crates", "algorithm", "time", "length", "map_string"])
    
    
    # Zamenji for loop range ce hocs kej vec al manj ampak 11 je zame nekje limit
    for map_id in range(1, 11):
        size = 5 + map_id // 2        #velikost stpnevanje
        num_crates = 1 + map_id // 2  # vsaki 2 mapi se doda nova škatla pa cilj
        custom_map = generate_custom_map(size, num_crates)
    
        env = gym.make("famnit_gym/Sokoban-v1", render_mode=None, options={"map_template": custom_map})
        observation, info = env.reset()
    
        player, crates, targets = get_player_crate_target_position(observation)
    
        # A* del
        start = time.time()
        a_star_solution = astar(player, crates, targets, observation)
        a_star_time = time.time() - start
        a_star_length = len(a_star_solution) if a_star_solution is not None else 0
    
        # DFS del
        start = time.time()
        dfs_solution = dfs(player, crates, targets, observation)
        dfs_time = time.time() - start
        dfs_length = len(dfs_solution) if dfs_solution is not None else 0
    
        # BFS del
        start = time.time()
        bfs_solution = bfs(player, crates, targets, observation)
        bfs_time = time.time() - start
        bfs_length = len(bfs_solution) if bfs_solution is not None else 0
    
        env.close()
    
        #Ustvari results
        
        map_string = f'[{";".join([" ".join(map(str, row)) for row in observation])}]'
    
        with open(csv_file, mode="a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([map_id, size, num_crates, "A*", a_star_time, a_star_length, map_string])
            writer.writerow([map_id, size, num_crates, "DFS", dfs_time, dfs_length, map_string])
            writer.writerow([map_id, size, num_crates, "BFS", bfs_time, bfs_length, map_string])
    
        print(f"Map {map_id} (size={size}, crates={num_crates}) done.")
