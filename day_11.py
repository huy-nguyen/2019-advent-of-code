from day_05 import compile_source_code, MessageType
from collections import namedtuple
from typing import Tuple, List
from enum import Enum, unique, auto
import itertools

Coord = namedtuple("Coord", ["x", "y"])
Panel = namedtuple("Panel", ["is_painted", "color"])


@unique
class Direction(Enum):
    UP = auto()
    RIGHT = auto()
    DOWN = auto()
    LEFT = auto()


class Board:
    def __init__(self, initial_panel_color: int):
        self.__board = {Coord(x=0, y=0): Panel(
            is_painted=False, color=initial_panel_color)}

    def __getitem__(self, key):
        default_panel = Panel(is_painted=False, color=0)
        if isinstance(key, Coord):
            if key in self.__board:
                return self.__board[key].color
            else:
                self.__board[key] = default_panel
                return default_panel.color
        else:
            raise TypeError(f"Key {key} is not a two-tuple of integers.")

    def __setitem__(self, key, value):
        if isinstance(key, Coord):
            new_value = Panel(is_painted=True, color=value)
            self.__board[key] = new_value
        else:
            raise TypeError(f"Key {key} is not a two-tuple of integers.")

    def get_printable_representation(self) -> List[str]:
        board = self.__board
        black_marker = " "
        white_marker = "X"
        all_xs = [position.x for position in board.keys()]
        all_ys = [abs(position.y) for position in board.keys()]
        max_x = max(all_xs)
        max_y = max(all_ys)

        num_rows = max_y + 1
        num_columns = max_x + 1
        buffer: List[List[str]] = [[black_marker]
                                   * num_columns for x in range(num_rows)]
        for (x, y), panel in board.items():
            buffer[-y][x] = black_marker if panel.color == 0 else white_marker

        return ["".join(line) for line in buffer]

    def get_num_panels_painted_at_least_once(self):
        painted_panels = [
            panel for panel in self.__board.values() if panel.is_painted == True]
        return len(painted_panels)


left_turn = {
    Direction.UP: Direction.LEFT,
    Direction.LEFT: Direction.DOWN,
    Direction.DOWN: Direction.RIGHT,
    Direction.RIGHT: Direction.UP
}
right_turn = {
    Direction.UP: Direction.RIGHT,
    Direction.LEFT: Direction.UP,
    Direction.DOWN: Direction.LEFT,
    Direction.RIGHT: Direction.DOWN
}


def move_in_direction(point: Coord, direction: Direction) -> Coord:
    if direction == Direction.UP:
        return Coord(x=point.x, y=point.y + 1)
    elif direction == Direction.RIGHT:
        return Coord(x=point.x + 1, y=point.y)
    elif direction == Direction.DOWN:
        return Coord(x=point.x, y=point.y - 1)
    else:
        return Coord(x=point.x - 1, y=point.y)


def run_program(source_code: str, initial_panel_color: int):
    board = Board(initial_panel_color)
    program = compile_source_code(source_code)

    should_continue = True
    message = next(program)
    consecutive_output_message_count = 0
    position = Coord(x=0, y=0)
    direction = Direction.UP

    while should_continue:
        if message.type == MessageType.GET_INPUT:
            message = program.send(board[position])
            consecutive_output_message_count = 0
        elif message.type == MessageType.PRINT_OUTPUT:
            if consecutive_output_message_count == 0:
                # This must be the color instruction:
                board[position] = message.arg
            elif consecutive_output_message_count == 1:
                # This must be the movement instruction:
                next_direction = left_turn[direction] if message.arg == 0 else right_turn[direction]
                next_position = move_in_direction(position, next_direction)
                position = next_position
                direction = next_direction
            else:
                raise RuntimeError(
                    f"There should not be more than 2 consecutive output calls. Receive {consecutive_output_message_count} calls.")
            consecutive_output_message_count += 1
            message = next(program)
        elif message.type == MessageType.TERMINATE:
            should_continue = False
    return board


def part_one():
    with open("day_11_input.txt") as f:
        source_code = f.readline()
        board = run_program(source_code, 0)
        return board.get_num_panels_painted_at_least_once()

def part_two():
    with open("day_11_input.txt") as f:
        source_code = f.readline()
        board = run_program(source_code, 1)
        buffer = board.get_printable_representation()
        for line in buffer:
            print(line)

# Note: These tests are commented out because the input and expected output are
# different for each Advent of Code participant. The tests as written below
# pass given my input and the correct output (as judged by the AoC website).
# def test_part_one():
#     assert part_one() == 1951

if __name__ == "__main__":
    part_two()
