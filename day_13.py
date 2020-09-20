from enum import Enum, unique, auto
from typing import Tuple, List, Dict
from collections import namedtuple
from day_05 import compile_source_code, MessageType
import re
import readchar

Coord = namedtuple("Coord", ["x", "y"])
Tile = namedtuple("Tile", ["id"])


@unique
class TileId(Enum):
    EMPTY = auto()
    WALL = auto()
    BLOCK = auto()
    HORIZONTAL_PADDLE = auto()
    BALL = auto()


int_to_tile_id = {
    0: TileId.EMPTY,
    1: TileId.WALL,
    2: TileId.BLOCK,
    3: TileId.HORIZONTAL_PADDLE,
    4: TileId.BALL,
}


tile_id_to_str = {
    TileId.EMPTY: " ",
    TileId.WALL: "W",
    TileId.BLOCK: "X",
    TileId.HORIZONTAL_PADDLE: "\u2588",
    TileId.BALL: "O",

}


class Screen:
    def __init__(self):
        self.__screen: Dict[Coord, Tile] = {}

    def __getitem__(self, key):
        if isinstance(key, Coord):
            return self.__screen[key].id
        else:
            raise TypeError(f"Key {key} is not a two-tuple of integers.")

    def __setitem__(self, key, value):
        if isinstance(key, Coord) and isinstance(value, TileId):
            new_value = Tile(id=value)
            self.__screen[key] = new_value
        else:
            raise TypeError(
                f"Key {key} is not a two-tuple of integers or value {value} is not a tile ID")

    def get_num_block_tiles(self):
        return len([x for x in self.__screen.values() if x.id == TileId.BLOCK])

    def __str__(self):
        screen = self.__screen

        all_xs = [position.x for position in screen.keys()]
        all_ys = [position.y for position in screen.keys()]
        max_x = max(all_xs)
        max_y = max(all_ys)

        num_rows = max_y + 1
        num_cols = max_x + 1

        buffer: List[List[str]] = [[tile_id_to_str[TileId.EMPTY]]
                                   * num_cols for _ in range(num_rows)]

        for (x, y), tile in screen.items():
            tile_id = tile.id

            if tile_id == TileId.WALL:
                if y == 0:
                    char = "\u2581"
                elif y == max_y:
                    char = "\u2594"
                elif x == 0:
                    char = "\u2595"
                else:
                    char = "\u258F"
            else:
                char = tile_id_to_str[tile_id]
            buffer[y][x] = char

        return "\n".join(["".join(line) for line in buffer])


keyboard_to_joystick_position = {
    "a": -1,  # Left
    "s": 0,  # Neutral
    "\r": 0,  # Neutral
    "d": 1,  # Right
    "j": -1,  # Left
    "k": 0,  # Neutral
    "l": 1,  # Right
}


def run_program(source_code: str, get_user_input, num_quarters=None):
    modified_source_code = re.sub(
        "^(\d+)", str(int(num_quarters)), source_code) if num_quarters is not None else source_code
    screen = Screen()
    program = compile_source_code(modified_source_code)

    should_continue = True
    message = next(program)
    output_message_count = 0
    x = 0
    y = 0
    score = 0

    while should_continue:
        if message.type == MessageType.GET_INPUT:
            print(screen, "\n")
            user_input = keyboard_to_joystick_position[get_user_input(
                message.arg)]
            message = program.send(user_input)
        if message.type == MessageType.PRINT_OUTPUT:
            if output_message_count % 3 == 0:
                x = message.arg
            elif output_message_count % 3 == 1:
                y = message.arg
            elif output_message_count % 3 == 2:
                if x == -1 and y == 0:
                    score = message.arg
                    print(f"Score: {score}")
                else:
                    tile_id = int_to_tile_id[message.arg]
                    screen[Coord(x=x, y=y)] = tile_id
            output_message_count += 1
            message = next(program)
        elif message.type == MessageType.TERMINATE:
            if score == 0:
                print("GAME OVER")
            should_continue = False
        else:
            raise RuntimeError(
                f"Unknown or unexpected message type {message.type}")
    return screen


def part_one():
    with open("day_13_input.txt") as f:
        source_code = f.readline()
        screen, _ = run_program(source_code, input)
        return screen.get_num_block_tiles()


# Note: These tests are commented out because the input and expected output are
# different for each Advent of Code participant. The tests as written below
# pass given my input and the correct output (as judged by the AoC website).
# def test_part_one():
#     assert part_one() == 200


def read_single_char_from_stdin(_):
    return readchar.readchar()


def part_two():
    with open("day_13_input.txt") as f:
        source_code = f.readline()
        print("""
Instruction:
Press "a" o "j" to move the paddle left.
Press "d" or "l" to move the paddle right.
Press "s", "k" or "Enter" to keep it in the same position.
""")
        screen = run_program(source_code, read_single_char_from_stdin, 2)
        return screen.get_num_block_tiles()


if __name__ == "__main__":
    part_two()
