from typing import Tuple, Union, List, Set
from enum import Enum, unique, auto
import pprint
import itertools


@unique
class Line_Orientation(Enum):
    VERTICAL = auto()
    HORIZONTAL = auto()


Point = Tuple[int, int]


def manhattan_distance(point_one: Point, point_two: Point) -> int:
    (x1, y1) = point_one
    (x2, y2) = point_two
    return abs(x1 - x2) + abs(y1 - y2)


def is_in_interval_inclusive(value: int, interval: Tuple[int, int]) -> bool:
    lower, upper = interval if interval[0] <= interval[1] else (
        interval[1], interval[0])
    return value <= upper and value >= lower


class Line:
    def __init__(self, start: Point, end: Point):
        (x1, y1) = start
        (x2, y2) = end
        if x1 == x2 and y1 == y2:
            raise RuntimeError("Line must have non-zero length")
        self.start = start
        self.end = end

    def __str__(self):
        x1, y1 = self.start
        x2, y2 = self.end
        return f'[({x1}, {y1}) to ({x2}, {y2})]'

    def length(self) -> int:
        return manhattan_distance(self.start, self.end)

    def get_orientation(self) -> Line_Orientation:
        x1, _ = self.start
        x2, _ = self.end
        if x1 == x2:
            return Line_Orientation.VERTICAL
        else:
            return Line_Orientation.HORIZONTAL


def get_intersection_between_lines(us: Line, them: Line) -> Union[None, Point]:
    our_orientation = us.get_orientation()
    their_orientation = them.get_orientation()
    # Here we assume that lines that may intersect at any point
    # are never co-linear i.e. they are not on the same infinte line:
    if (our_orientation == their_orientation):
        return None
    else:
        horizontal_line, vertical_line = (
            us, them) if our_orientation == Line_Orientation.HORIZONTAL else (them, us)
        x1_horizontal, y_horizontal = horizontal_line.start
        x2_horizontal, _ = horizontal_line.end
        x_vertical, y1_vertical = vertical_line.start
        _, y2_vertical = vertical_line.end
        if is_in_interval_inclusive(x_vertical, (x1_horizontal, x2_horizontal)) and is_in_interval_inclusive(y_horizontal, (y1_vertical, y2_vertical)):
            return (x_vertical, y_horizontal)
        else:
            return None


Path = List[Line]
Instruction = Tuple[str, int]


def parse_into_path(raw_input: str) -> Path:
    input: List[Instruction] = [(x[:1], int(x[1:]))
                                for x in raw_input.split(',')]
    current_point: Point = (0, 0)
    path: Path = []
    # Regular right-handed coords: +x is right, +y is up:
    for direction, distance in input:
        prevX, prevY = current_point
        if direction == "U":
            nextX = prevX
            nextY = prevY + distance
            next_point = (nextX, nextY)
            nextLine = Line(current_point, next_point)
            path.append(nextLine)
            current_point = next_point
        elif direction == "D":
            nextX = prevX
            nextY = prevY - distance
            next_point = (nextX, nextY)
            nextLine = Line(current_point, next_point)
            path.append(nextLine)
            current_point = next_point
        elif direction == "L":
            nextX = prevX - distance
            nextY = prevY
            next_point = (nextX, nextY)
            nextLine = Line(current_point, next_point)
            path.append(nextLine)
            current_point = next_point
        elif direction == "R":
            nextX = prevX + distance
            nextY = prevY
            next_point = (nextX, nextY)
            nextLine = Line(current_point, next_point)
            path.append(nextLine)
            current_point = next_point
        else:
            raise RuntimeError("Invalid movement direction " + direction)
    return path


origin: Point = (0, 0)


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
    if line_orientation == Line_Orientation.HORIZONTAL:
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
