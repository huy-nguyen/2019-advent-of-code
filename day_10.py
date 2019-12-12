from typing import Tuple, List
from collections import namedtuple
import itertools
import pytest
import math
from math import pi
from fractions import Fraction
from more_itertools import partition

Asteroid: Tuple[int, int] = namedtuple("Asteroid", ["x", "y"])
Point: Tuple[int, int] = namedtuple("Point", ["x", "y"])
Vector: Tuple[int, int] = namedtuple("Vector", ["x", "y"])
Line: Tuple[Point, Point] = namedtuple("Line", ["start", "end"])


empty_marker = "."
asteroid_marker = "#"


def get_asteroid_from_text_lines(lines: List[str]) -> List[Asteroid]:
    result: List[Asteroid] = []
    for y, line in enumerate(lines):
        for x, character in enumerate(line):
            if character == asteroid_marker:
                result.append(Asteroid(x=x, y=y))
    return result


input_1 = """
.#..#
.....
#####
....#
...##
""".strip().splitlines()


def test_get_asteroid_from_text_lines():
    assert get_asteroid_from_text_lines(input_1) == [
        Asteroid(x=1, y=0),
        Asteroid(x=4, y=0),
        Asteroid(x=0, y=2),
        Asteroid(x=1, y=2),
        Asteroid(x=2, y=2),
        Asteroid(x=3, y=2),
        Asteroid(x=4, y=2),
        Asteroid(x=4, y=3),
        Asteroid(x=3, y=4),
        Asteroid(x=4, y=4),
    ]


def are_vector_cross_product_zero(a: Vector, b: Vector) -> bool:
    return a.x * b.y - a.y * b.x == 0


def test_are_vector_cross_product_zero():
    assert are_vector_cross_product_zero(
        Vector(x=1, y=2), Vector(x=2, y=4)) == True
    assert are_vector_cross_product_zero(
        Vector(x=1, y=2), Vector(x=1, y=3)) == False


def dot_product(a: Vector, b: Vector) -> int:
    return a.x * b.x + a.y * b.y


def is_line_of_slight_obstructed_by(start: Asteroid, end: Asteroid, obstruction: Asteroid) -> bool:
    if start.x == end.x and start.y == end.y:
        return False
    else:
        # This check is based on https://lucidar.me/en/mathematics/check-if-a-point-belongs-on-a-line-segment/
        start_end_vector = Vector(
            x=end.x - start.x, y=end.y - start.y)
        start_asteroid_vector = Vector(
            x=obstruction.x - start.x, y=obstruction.y - start.y)
        cross_product_is_zero = are_vector_cross_product_zero(
            start_end_vector, start_asteroid_vector)
        dot_product_1 = dot_product(start_end_vector, start_asteroid_vector)
        dot_product_2 = dot_product(start_end_vector, start_end_vector)
        return cross_product_is_zero and dot_product_2 > dot_product_1 and dot_product_1 > 0


def test_is_line_of_slight_obstructed_by():
    assert is_line_of_slight_obstructed_by(
        Asteroid(x=3, y=4), Asteroid(x=1, y=0), Asteroid(x=2, y=2)) == True
    assert is_line_of_slight_obstructed_by(
        Asteroid(x=3, y=4), Asteroid(x=1, y=0), Asteroid(x=3, y=2)) == False


def get_line_of_sight_count(me: Asteroid, them: List[Asteroid]) -> int:
    count = 0
    for target_index, target in enumerate(them):
        for obstruction_index, obstruction in enumerate(them):
            if obstruction_index != target_index and is_line_of_slight_obstructed_by(me, target, obstruction):
                break
        else:
            count += 1
    return count


@pytest.mark.parametrize(
    "asteroid_index,expected_count",
    [
        (0, 7),
        (1, 7),
        (2, 6),
        (3, 7),
        (4, 7),
        (5, 7),
        (6, 5),
        (7, 7),
        (8, 8),
        (9, 7)
    ]
)
def test_get_line_of_sight_count(asteroid_index, expected_count):
    asteroids = get_asteroid_from_text_lines(input_1)
    assert get_line_of_sight_count(
        asteroids[asteroid_index], asteroids[:asteroid_index] + asteroids[asteroid_index + 1:]) == expected_count


def find_best_asteroid(lines: List[str]):
    asteroids = get_asteroid_from_text_lines(lines)
    max_line_of_sight_count = - float("inf")
    max_line_of_sight_asteroid = None
    for index, asteroid in enumerate(asteroids):
        count = get_line_of_sight_count(
            asteroid, asteroids[:index] + asteroids[index + 1:])
        if count > max_line_of_sight_count:
            max_line_of_sight_count = count
            max_line_of_sight_asteroid = asteroid
    return max_line_of_sight_count, max_line_of_sight_asteroid


input_2 = """
......#.#.
#..#.#....
..#######.
.#.#.###..
.#..#.....
..#....#.#
#..#....#.
.##.#..###
##...#..#.
.#....####
""".strip().splitlines()

input_3 = """
#.#...#.#.
.###....#.
.#....#...
##.#.#.#.#
....#.#.#.
.##..###.#
..#...##..
..##....##
......#...
.####.###.
""".strip().splitlines()

input_4 = """
.#..#..###
####.###.#
....###.#.
..###.##.#
##.##.#.#.
....###..#
..#.#..#.#
#..#.#.###
.##...##.#
.....#.#..
""".strip().splitlines()

input_5 = """
.#..##.###...#######
##.############..##.
.#.######.########.#
.###.#######.####.#.
#####.##.#.##.###.##
..#####..#.#########
####################
#.####....###.#.#.##
##.#################
#####.##.###..####..
..######..##.#######
####.##.####...##..#
.#####..#.######.###
##...#.##########...
#.##########.#######
.####.#.###.###.#.##
....##.##.###..#####
.#.#.###########.###
#.#.#.#####.####.###
###.##.####.##.#..##
""".strip().splitlines()


@pytest.mark.parametrize(
    "lines,expected",
    [
        (input_2, (33, Asteroid(x=5, y=8))),
        (input_3, (35, Asteroid(x=1, y=2))),
        (input_4, (41, Asteroid(x=6, y=3))),
        (input_5, (210, Asteroid(x=11, y=13))),
    ]
)
def test_find_best_asteroid(lines, expected):
    assert find_best_asteroid(lines) == expected


def part_one():
    with open("day_10_input.txt") as f:
        lines = [x.strip() for x in f]
        return find_best_asteroid(lines)


def test_part_one():
    assert part_one() == (309, Asteroid(x=37, y=25))


def get_vertical_reference_vector(origin: Point) -> Vector:
    """The vector origin -> return_value is the upward pointing unit vector in the coord system centered on origin."""
    return Vector(x=origin.x, y=origin.y - 1)

# Adapted from https://stackoverflow.com/a/16544330/7075699
def get_clockwise_angle_btw_vectors(v1: Vector, v2: Vector, origin: Point) -> float:
    """Get clockwise angle in [0, 2 * pi) between v1 and v2"""
    adjusted_v1 = Vector(x=(v1.x - origin.x), y=-(-v1.y + origin.y))
    adjusted_v2 = Vector(x=(v2.x - origin.x), y=-(-v2.y + origin.y))
    dot = adjusted_v1.x * adjusted_v2.x + adjusted_v1.y * adjusted_v2.y
    det = adjusted_v1.x * adjusted_v2.y - adjusted_v1.y * adjusted_v2.x
    unadjusted = math.atan2(det, dot)
    result = unadjusted if unadjusted >= 0 else 2 * pi + unadjusted
    return result


def get_clockwise_angle_from_vertical(v: Vector, origin: Point) -> float:
    vertical = get_vertical_reference_vector(origin)
    return get_clockwise_angle_btw_vectors(vertical, v, origin)


@pytest.mark.parametrize(
    "origin, vector, expected_angle",
    [
        (Point(x=0, y=0), Vector(0, -1), 0),
        (Point(x=0, y=0), Vector(1, -1), pi / 4),
        (Point(x=0, y=0), Vector(1, 0), pi / 2),
        (Point(x=0, y=0), Vector(1, 1), 3 * pi / 4),
        (Point(x=0, y=0), Vector(0, 1), pi),
        (Point(x=0, y=0), Vector(-1, 1), 5 * pi / 4),
        (Point(x=0, y=0), Vector(-1, 0), 3 * pi / 2),
        (Point(x=0, y=0), Vector(-1, -1), 7 * pi / 4),

        # Same points as above but in shifted coord system:
        (Point(x=1, y=2), Vector(1, 1), 0),
        (Point(x=1, y=2), Vector(2, 1), pi / 4),
        (Point(x=1, y=2), Vector(2, 2), pi / 2),
    ]
)
def test_get_clockwise_angle_from_vertical(origin, vector, expected_angle):
    assert get_clockwise_angle_from_vertical(vector, origin) == expected_angle


input_6 = """
.#....#####...#..
##...##.#####..##
##...#...#.#####.
..#.....#...###..
..#.#.....#....##
""".strip().splitlines()


def get_distance_from_origin(asteroid: Asteroid, origin: Point) -> float:
    return math.sqrt(
        (asteroid.x - origin.x) ** 2 +
        (asteroid.y - origin.y) ** 2
    )


def sort_by_vaporization_order(asteroids: List[Asteroid], origin: Point) -> List[Asteroid]:
    # Remove the asteroid at the origin from consideration:
    with_asteroid_at_origin_removed = [
        a for a in asteroids if not (a.x == origin.x and a.y == origin.y)]

    sorted_by_clock_angle = sorted(
        with_asteroid_at_origin_removed,
        key=lambda asteroid: get_clockwise_angle_from_vertical(
            Vector(x=asteroid.x, y=asteroid.y),
            origin
        )
    )

    grouped_by_clock_angle: List[List[Asteroid]] = []
    last_asteroid_clock_angle = None
    current_group: List[Asteroid] = []
    for asteroid in sorted_by_clock_angle:
        current_clock_angle = get_clockwise_angle_from_vertical(
            Vector(x=asteroid.x, y=asteroid.y), origin)
        if last_asteroid_clock_angle is not None and not math.isclose(current_clock_angle, last_asteroid_clock_angle):
            grouped_by_clock_angle.append(current_group)
            current_group = []
        current_group.append(asteroid)
        last_asteroid_clock_angle = current_clock_angle
    if len(current_group) > 0:
        grouped_by_clock_angle.append(current_group)

    sorted_by_clock_angle_and_distance: List[List[Asteroid]] = []
    for asteroids_at_same_line_of_sight in grouped_by_clock_angle:
        sorted_asteroids = sorted(asteroids_at_same_line_of_sight,
                                  key=lambda asteroid: get_distance_from_origin(asteroid, origin))
        sorted_by_clock_angle_and_distance.append(sorted_asteroids)

    vaporization_order: List[Asteroid] = []
    for asteroids_in_same_vaporization_pass in itertools.zip_longest(*sorted_by_clock_angle_and_distance):
        vaporization_order.extend(
            [x for x in asteroids_in_same_vaporization_pass if x is not None])
    return vaporization_order


def test_sort_by_vaporization_order_1():
    asteroids = get_asteroid_from_text_lines(input_6)
    vaporization_order = sort_by_vaporization_order(asteroids, Point(x=8, y=3))
    assert vaporization_order == [
        # First 9:
        Asteroid(x=8, y=1),  # 1
        Asteroid(x=9, y=0),
        Asteroid(x=9, y=1),
        Asteroid(x=10, y=0),
        Asteroid(x=9, y=2),  # 5
        Asteroid(x=11, y=1),
        Asteroid(x=12, y=1),
        Asteroid(x=11, y=2),
        Asteroid(x=15, y=1),  # 9
        # Next 9:
        Asteroid(x=12, y=2),  # 1
        Asteroid(x=13, y=2),
        Asteroid(x=14, y=2),
        Asteroid(x=15, y=2),
        Asteroid(x=12, y=3),  # 5
        Asteroid(x=16, y=4),
        Asteroid(x=15, y=4),
        Asteroid(x=10, y=4),
        Asteroid(x=4, y=4),  # 9
        # Next 9:
        Asteroid(x=2, y=4),  # 1
        Asteroid(x=2, y=3),
        Asteroid(x=0, y=2),
        Asteroid(x=1, y=2),
        Asteroid(x=0, y=1),  # 5
        Asteroid(x=1, y=1),
        Asteroid(x=5, y=2),
        Asteroid(x=1, y=0),
        Asteroid(x=5, y=1),  # 9
        # Last 9
        Asteroid(x=6, y=1),  # 1
        Asteroid(x=6, y=0),
        Asteroid(x=7, y=0),
        Asteroid(x=8, y=0),
        Asteroid(x=10, y=1),  # 5
        Asteroid(x=14, y=0),
        Asteroid(x=16, y=1),
        Asteroid(x=13, y=3),
        Asteroid(x=14, y=3),  # 9
    ]


def test_sort_by_vaporization_order_2():
    asteroids = get_asteroid_from_text_lines(input_5)
    vaporization_order = sort_by_vaporization_order(
        asteroids, Point(x=11, y=13))
    assert vaporization_order[0] == Asteroid(x=11, y=12)
    assert vaporization_order[1] == Asteroid(x=12, y=1)
    assert vaporization_order[2] == Asteroid(x=12, y=2)
    assert vaporization_order[9] == Asteroid(x=12, y=8)
    assert vaporization_order[19] == Asteroid(x=16, y=0)
    assert vaporization_order[49] == Asteroid(x=16, y=9)
    assert vaporization_order[99] == Asteroid(x=10, y=16)
    assert vaporization_order[198] == Asteroid(x=9, y=6)
    assert vaporization_order[199] == Asteroid(x=8, y=2)
    assert vaporization_order[200] == Asteroid(x=10, y=9)
    assert vaporization_order[298] == Asteroid(x=11, y=1)


def part_two():
    with open("day_10_input.txt") as f:
        lines = [x.strip() for x in f]
        asteroids = get_asteroid_from_text_lines(lines)
        origin = Point(x=37, y=25)
        vaporization_order = sort_by_vaporization_order(asteroids, origin)
        asteroid_200th = vaporization_order[199]
        return asteroid_200th.x * 100 + asteroid_200th.y


def test_part_two():
    assert part_two() == 416


if __name__ == "__main__":
    pass
