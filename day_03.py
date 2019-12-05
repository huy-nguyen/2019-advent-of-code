from typing import Tuple, Union, List, Set
from enum import Enum, unique, auto
import pprint
import itertools
from collections import namedtuple


@unique
class Orientation(Enum):
    VERTICAL = auto()
    HORIZONTAL = auto()


Point: Tuple[int, int] = namedtuple('Point', ['x', 'y'])


def manhattan_distance(point_one: Point, point_two: Point) -> int:
    return abs(point_one.x - point_two.x) + abs(point_one.y - point_two.y)


def is_in_interval_inclusive(value: int, interval: Tuple[int, int]) -> bool:
    lower, upper = interval if interval[0] <= interval[1] else (
        interval[1], interval[0])
    return value <= upper and value >= lower


class Line:
    def __init__(self, start: Point, end: Point):
        if start.x == end.x and start.y == end.y:
            raise RuntimeError("Line must have non-zero length")
        self.start = start
        self.end = end

    def __str__(self):
        start, end = self.start, self.end
        return f'[({start.x}, {start.y}) to ({end.x}, {end.y})]'

    def length(self) -> int:
        return manhattan_distance(self.start, self.end)

    def get_orientation(self) -> Orientation:
        start, end = self.start, self.end
        if start.x == end.x:
            return Orientation.VERTICAL
        else:
            return Orientation.HORIZONTAL


def get_intersection_between_lines(us: Line, them: Line) -> Union[None, Point]:
    our_orientation = us.get_orientation()
    their_orientation = them.get_orientation()
    # Here we assume that lines that may intersect at any point
    # are never co-linear i.e. they are not on the same infinte line:
    if our_orientation == their_orientation:
        return None
    else:
        horizontal_line, vertical_line = (
            us, them) if our_orientation == Orientation.HORIZONTAL else (them, us)
        x1_horizontal, y_horizontal = horizontal_line.start
        x2_horizontal, _ = horizontal_line.end
        x_vertical, y1_vertical = vertical_line.start
        _, y2_vertical = vertical_line.end
        if is_in_interval_inclusive(x_vertical, (x1_horizontal, x2_horizontal)) and is_in_interval_inclusive(y_horizontal, (y1_vertical, y2_vertical)):
            return Point(x_vertical, y_horizontal)
        else:
            return None


Path = List[Line]
Instruction: Tuple[str, int] = namedtuple('Instruction', ['direction', 'distance'])


def parse_into_path(raw_input: str) -> Path:
    input: List[Instruction] = [Instruction(direction=x[:1], distance=int(x[1:]))
                                for x in raw_input.split(',')]
    current_point: Point = Point(0, 0)
    path: Path = []
    # Regular right-handed coords: +x points to the right, +y is up:
    for direction, distance in input:
        prevX, prevY = current_point
        if direction == "U":
            nextX = prevX
            nextY = prevY + distance
            next_point = Point(nextX, nextY)
            nextLine = Line(current_point, next_point)
            path.append(nextLine)
            current_point = next_point
        elif direction == "D":
            nextX = prevX
            nextY = prevY - distance
            next_point = Point(nextX, nextY)
            nextLine = Line(current_point, next_point)
            path.append(nextLine)
            current_point = next_point
        elif direction == "L":
            nextX = prevX - distance
            nextY = prevY
            next_point = Point(nextX, nextY)
            nextLine = Line(current_point, next_point)
            path.append(nextLine)
            current_point = next_point
        elif direction == "R":
            nextX = prevX + distance
            nextY = prevY
            next_point = Point(nextX, nextY)
            nextLine = Line(current_point, next_point)
            path.append(nextLine)
            current_point = next_point
        else:
            raise RuntimeError("Invalid movement direction " + direction)
    return path


origin = Point(0, 0)


def get_all_intersections(us: Path, them: Path) -> List[Point]:
    all_intersections: List[Point] = []
    for our_line, their_line in itertools.product(us, them):
        intersection = get_intersection_between_lines(our_line, their_line)
        if intersection is not None:
            all_intersections.append(intersection)
    return [x for x in all_intersections if x != origin]


def get_intersection_closest_to_origin(us: Path, them: Path) -> int:
    distances = [manhattan_distance(x, origin)
                 for x in get_all_intersections(us, them)]
    shortest_distance = min(distances)
    return shortest_distance


def part_one():
    with open("day_03_input.txt") as f:
        raw_first_line = f.readline()
        raw_second_line = f.readline()
        parsed_first_line = parse_into_path(raw_first_line)
        parsed_second_line = parse_into_path(raw_second_line)
        return get_intersection_closest_to_origin(parsed_first_line, parsed_second_line)


def is_point_on_line(point: Point, line: Line) -> bool:
    point_x, point_y = point
    line_orientation = line.get_orientation()
    if line_orientation == Orientation.HORIZONTAL:
        x1, line_y = line.start
        x2, _ = line.end
        return is_in_interval_inclusive(point_x, (x1, x2)) and point_y == line_y
    else:
        line_x, y1 = line.start
        _, y2 = line.end
        return is_in_interval_inclusive(point_y, (y1, y2)) and point_x == line_x


def get_distance_from_path_start(point: Point, path: Path) -> int:
    distance = 0
    for line in path:
        if is_point_on_line(point, line):
            distance += manhattan_distance(line.start, point)
            break
        else:
            distance += line.length()
    else:
        raise RuntimeError(f'Point {point} is not on line {line}')
    return distance


def get_shortest_total_distance_along_paths(us: Path, them: Path) -> int:
    distances = [
        get_distance_from_path_start(x, us) +
        get_distance_from_path_start(x, them)
        for x in get_all_intersections(us, them)]
    return min(distances)


def part_two():
    with open("day_03_input.txt") as f:
        raw_first_line = f.readline()
        raw_second_line = f.readline()
        parsed_first_line = parse_into_path(raw_first_line)
        parsed_second_line = parse_into_path(raw_second_line)
        return get_shortest_total_distance_along_paths(parsed_first_line, parsed_second_line)
