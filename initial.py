import gymnasium as gym
import famnit_gym
import numpy as np
# Create and reset the environment.


# ta array je za delat mapo
# 1 je zid, 5 je player, 2 je skatla in 3 je cilj
custom_map = np.array([
    [1, 1, 1, 1, 1],
    [1, 5, 0, 0, 1],
    [1, 0, 2, 0, 1],
    [1, 0, 0, 3, 1],
    [1, 1, 1, 1, 1],
], dtype=np.uint8)

env = gym.make('famnit_gym/Sokoban-v1', render_mode='human', options={'map_template': custom_map})
observation, info = env.reset()



# Execute random actions.
done = False
while not done:
    action = env.action_space.sample()
    _, _, terminated, truncated, _ = env.step(action)
    done = terminated or truncated
