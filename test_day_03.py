from day_03 import manhattan_distance, Line, get_intersection_between_lines, parse_into_path, get_intersection_closest_to_origin, part_one, get_distance_from_path_start, get_shortest_total_distance_along_paths, part_two
from collections import Counter


def test_manhattan_distance():
    assert manhattan_distance((0, 0), (0, 0)) == 0
    assert manhattan_distance((1, 2), (4, 5)) == 6


def test_line():
    assert Line((1, 2), (4, 5)).length() == 6


def test_line_intersection():
    assert get_intersection_between_lines(
        Line((1, 1), (1, 4)),
        Line((2, 2), (2, 5))
    ) == None
    assert get_intersection_between_lines(
        Line((1, 1), (1, 4)),
        Line((0, 2), (3, 2))
    ) == (1, 2)
    assert get_intersection_between_lines(
        Line((1, 1), (4, 1)),
        Line((1, 4), (1, 1))
    ) == (1, 1)


def test_get_intersections():
    assert get_intersection_closest_to_origin(
        parse_into_path('R8,U5,L5,D3'),
        parse_into_path('U7,R6,D4,L4')
    ) == 6
    assert get_intersection_closest_to_origin(
        parse_into_path('R75,D30,R83,U83,L12,D49,R71,U7,L72'),
        parse_into_path('U62,R66,U55,R34,D71,R55,D58,R83')
    ) == 159
    assert get_intersection_closest_to_origin(
        parse_into_path('R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51'),
        parse_into_path('U98,R91,D20,R16,D67,R40,U7,R15,U6,R7')
    ) == 135


def test_part_one():
    assert part_one() == 5319


def test_get_distance_from_path_start():
    assert get_distance_from_path_start(
        (3, 3),
        parse_into_path('R8,U5,L5,D3')
    ) == 20
    assert get_distance_from_path_start(
        (3, 3),
        parse_into_path('U7,R6,D4,L4')
    ) == 20
    assert get_distance_from_path_start(
        (6, 5),
        parse_into_path('R8,U5,L5,D3')
    ) == 15
    assert get_distance_from_path_start(
        (6, 5),
        parse_into_path('U7,R6,D4,L4')
    ) == 15


def test_get_shortest_total_distance_along_paths():
    assert get_shortest_total_distance_along_paths(
        parse_into_path('R8,U5,L5,D3'),
        parse_into_path('U7,R6,D4,L4'),
    ) == 30
    assert get_shortest_total_distance_along_paths(
        parse_into_path('R75,D30,R83,U83,L12,D49,R71,U7,L72'),
        parse_into_path('U62,R66,U55,R34,D71,R55,D58,R83'),
    ) == 610
    assert get_shortest_total_distance_along_paths(
        parse_into_path('R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51'),
        parse_into_path('U98,R91,D20,R16,D67,R40,U7,R15,U6,R7'),
    ) == 410


def test_part_two():
    assert part_two() == 122514
