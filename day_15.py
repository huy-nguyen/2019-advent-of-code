from enum import IntEnum, unique, auto
from day_05 import compile_source_code, run_with_input_output, MessageType
from collections import deque
from collections import namedtuple

# `path` is a series of `Direction`s to get to that point from (0, 0)
Coord = namedtuple("Coord", ["x", "y", "path"])

# Note: clockwise order
class Direction(IntEnum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3


input_command_for_direction = {
    Direction.NORTH: "1",
    Direction.SOUTH: "2",
    Direction.WEST: "3",
    Direction.EAST: "4",
}

displacements_for_direction = {
    Direction.NORTH: (0, 1),
    Direction.SOUTH: (0, -1),
    Direction.EAST: (-1, 0),
    Direction.WEST: (1, 0),
}


def get_response_to_movement_command(program, direction: Direction) -> int:
    next(program)
    response = program.send(input_command_for_direction[direction])
    if response.type == MessageType.PRINT_OUTPUT:
        return response.arg
    else:
        raise ValueError("Should be an PRINT_OUTPUT message. Received ", response.type)


def traverse_breadth_first(program: str, should_terminate_at_oxygen_tank: bool) -> int:
    """
    If `should_terminate_at_oxygen_tank` is True, we stop the search when the oxygen tank is found
    and return the count and path to reach the tank. That will solve part one.
    If `should_terminate_at_oxygen_tank` is False, we will keep iterating until all accessible coords
    have been visited and return the count. This will solve part two.
    """
    count = 0
    queue = deque([Coord(x=0, y=0, path=[])])
    visited = set([(0, 0)])
    while len(queue) > 0:
        count += 1
        queue_length = len(queue)
        for _ in range(queue_length):
            # For each coord that needs to be visited:
            (x, y, path) = queue.popleft()
            # Get to that coord from the origin:
            for direction in path:
                response_3 = get_response_to_movement_command(program, direction)
                if response_3 == 0:
                    raise ValueError(
                        "Should always be possible to travel a path that has been previously traversed."
                    )
            # Then look around:
            for direction in Direction:
                displacement = displacements_for_direction[direction]
                new_x = x + displacement[0]
                new_y = y + displacement[1]
                if (new_x, new_y) not in visited:
                    visited.add((new_x, new_y))
                    response_2 = get_response_to_movement_command(program, direction)
                    if response_2 == 2 and should_terminate_at_oxygen_tank:
                        return (count, path + [direction])
                    elif response_2 == 0:
                        pass
                    else:
                        queue.append(Coord(x=new_x, y=new_y, path=path + [direction]))
                        # Go back to previous location:
                        opposite_direction = Direction(
                            (direction.value + 2) % len(Direction)
                        )
                        response_1 = get_response_to_movement_command(
                            program, opposite_direction
                        )
                        if response_1 == 0:
                            raise ValueError(
                                "Should always be possible to return to last location."
                            )
            # Return to origin:
            for direction in reversed(path):
                opposite_direction = Direction((direction.value + 2) % len(Direction))
                response_4 = get_response_to_movement_command(
                    program, opposite_direction
                )
                if response_4 == 0:
                    raise ValueError(
                        "Should always be possible to traverse path in the opposite direction."
                    )
    return (count - 1, None)


def part_one():
    with open("day_15_input.txt") as f:
        source_code = f.readline()
        program = compile_source_code(source_code)
        num_steps, path = traverse_breadth_first(
            program, should_terminate_at_oxygen_tank=True
        )
        path_values = [x.value for x in path]
        print(path_values)
        return num_steps


def part_two():
    with open("day_15_input.txt") as f:
        source_code = f.readline()
        program_1 = compile_source_code(source_code)
        # Note that after this run, the repair robot is at the oxygen tank:
        traverse_breadth_first(program_1, should_terminate_at_oxygen_tank=True)
        # Now we can do BFS from that oxygen tank location:
        oxygen_spread_time, _ = traverse_breadth_first(
            program_1, should_terminate_at_oxygen_tank=False
        )
        return oxygen_spread_time


# Note: These tests are commented out because the input and expected output are
# different for each Advent of Code participant. The tests as written below
# pass given my input and the correct output (as judged by the AoC website).
# def test_part_one():
#     assert part_one() == 304
# def test_part_two():
#     assert part_two() == 310
