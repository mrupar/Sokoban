import gymnasium as gym
import famnit_gym
import numpy as np
import time
import csv

from informed_search import astar
from DFS import dfs
from BFS import bfs

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

# Generacija map
def generate_custom_map(size):
    """

        1 = zid
        0 = prazno
        5 = player
        2 = skatla
        3 = cilj
    """
    #stena okoli in prazna notranjost
    map_array = np.ones((size, size), dtype=np.uint8)  
    map_array[1:-1, 1:-1] = 0  

    # player je vedno levo zgori
    map_array[1, 1] = 5

    # skatla in cilna pozicja je dana diagonalno k gledamo sam velikost zdej
    if size > 3:
        map_array[2, 2] = 2
        map_array[size-2, size-2] = 3

    return map_array


if __name__ == "__main__":
    csv_file = "results_custom_map_size.csv"
    
    with open(csv_file, mode="w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["map_id", "map_size", "algorithm", "time", "length", "map_string"])
    
    #  Zamenji for loop range ce hocs kej vec al manj ampak 51 je zame nekje limit
    for map_id in range(1, 51):
        size = 5 + map_id // 2  #velikost stpnevanje
        custom_map = generate_custom_map(size)
    
        env = gym.make('famnit_gym/Sokoban-v1', render_mode=None, options={'map_template': custom_map})
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
            writer.writerow([map_id, size, "A*", a_star_time, a_star_length, map_string])
            writer.writerow([map_id, size, "DFS", dfs_time, dfs_length, map_string])
            writer.writerow([map_id, size, "BFS", bfs_time, bfs_length, map_string])
    
        print(f"Map {map_id} (size {size}) done.")
    