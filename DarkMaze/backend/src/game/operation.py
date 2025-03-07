from copy import deepcopy
from ..database.operation import save_game_state
from .judge import hit_obstacle, game_over, arrive_at_destination

GAME_WON_HEALTH = 666

def move_location(game_state, direction):
    if game_over(game_state["health"]):
        return game_state

    new_game_state = deepcopy(game_state)
    new_position = get_new_position(new_game_state["current_position"], direction, new_game_state["map_size"])

    if hit_obstacle(new_position, new_game_state["current_level_name"]):
        new_game_state["health"] -= 1
    else:
        update_position(new_game_state, new_position)

    if arrive_at_destination(new_game_state["current_level_name"], new_game_state["current_position"]):
        new_game_state["health"] = GAME_WON_HEALTH

    save_game_state_to_db(new_game_state)
    return new_game_state

def get_new_position(current_position, direction, map_size):
    x, y = current_position
    max_x, max_y = map_size

    moves = {
        "up": (x, max(y - 1, 0)),
        "down": (x, min(y + 1, max_y - 1)),
        "left": (max(x - 1, 0), y),
        "right": (min(x + 1, max_x - 1), y),
    }
    return moves.get(direction, current_position)

def update_position(game_state, new_position):
    if new_position not in game_state["path"]:
        game_state["path"].append(new_position)
    game_state["current_position"] = new_position

def save_game_state_to_db(game_state):
    save_game_state(
        game_state["username"],
        game_state["current_level_name"],
        game_state["map_size"],
        game_state["health"],
        game_state["path"],
        game_state["current_position"],
    )
