import numpy as np
import re
import json
from itertools import chain

GAME_OVER_HEALTH = {0, 666}

def _parse_map(map_string, map_size, reversal_nodes=[]):
    width, height = map_size
    map_chars = re.sub(r'[^a-zA-Z]', '', map_string)
    
    binary_values = [format(ord(c), '08b') for c in map_chars]
    flat_map = list(chain.from_iterable((int(b[:4], 2) % 2, int(b[4:], 2) % 2) for b in binary_values))

    flat_map.extend([0] * (width * height - len(flat_map)))
    flat_map = flat_map[:width * height]

    grid = np.array(flat_map).reshape((height, width))

    for x, y in reversal_nodes:
        if 0 <= x < height and 0 <= y < width:
            grid[y, x] ^= 1

    return grid

def _load_maze_from_json(maze_level_name):
    with open(f"./src/game/maze_level/{maze_level_name}.json", 'r', encoding='utf-8') as f:
        data = json.load(f)

    return {
        "maze_level_name": data.get("maze_level_name", "Unknown Level"),
        "map_size": tuple(data.get("map_size", [10, 10])),
        "starting_position": tuple(data.get("starting_position", [0, 0])),
        "end_position": tuple(data.get("end_position", [0, 0])),
        "map": _parse_map(data.get("map", ""), tuple(data.get("map_size", [10, 10])), data.get("reversal_node", []))
    }

def hit_obstacle(position, maze_level_name):
    x, y = position
    maze_data = _load_maze_from_json(maze_level_name)
    grid = maze_data["map"]

    if 0 <= x < grid.shape[0] and 0 <= y < grid.shape[1]:
        return grid[y, x] == 1 
    return True 

def game_over(health):
    return health in GAME_OVER_HEALTH

def arrive_at_destination(maze_level_name, current_position):
    """判斷是否到達終點"""
    maze_data = _load_maze_from_json(maze_level_name)
    return tuple(current_position) == maze_data["end_position"]
