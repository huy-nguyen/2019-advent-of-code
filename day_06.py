from typing import Dict, List, NamedTuple, Optional, Set
from collections import namedtuple, deque

OrbitsOfObject: NamedTuple(
    "OrbitsOfObject", [("direct", Optional[str]), ("indirect", List[str])]
) = namedtuple("OrbitsOfObject", ["direct", "indirect"])

sample_input_part_one = """COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L"""


def get_orbits_of_object(data: Dict[str, str], name: str):
    if name not in data:
        return OrbitsOfObject(direct=None, indirect=[])
    result = []
    next_name = data[name]
    result.append(next_name)
    while next_name in data:
        next_name = data[next_name]
        result.append(next_name)
    direct = result[0]
    indirect = result[1:]
    return OrbitsOfObject(direct=direct, indirect=indirect)


def test_get_orbits_of_object():
    data = parse_input_into_hash_table(sample_input_part_one.splitlines())
    assert get_orbits_of_object(data, "COM") == OrbitsOfObject(direct=None, indirect=[])
    assert get_orbits_of_object(data, "B") == OrbitsOfObject(direct="COM", indirect=[])
    assert get_orbits_of_object(data, "G") == OrbitsOfObject(
        direct="B", indirect=["COM"]
    )
    assert get_orbits_of_object(data, "L") == OrbitsOfObject(
        direct="K", indirect=["J", "E", "D", "C", "B", "COM"]
    )


def count_orbits(data: Dict[str, str]):
    total = 0
    for key in data:
        orbits = get_orbits_of_object(data, key)
        direct_count = 0 if orbits.direct is None else 1
        indirect_count = len(orbits.indirect)
        total += direct_count + indirect_count
    return total


def test_count_orbits():
    data = parse_input_into_hash_table(sample_input_part_one.splitlines())
    assert count_orbits(data) == 42


def part_one():
    with open("day_06_input.txt") as f:
        without_new_line_chars = [x.strip() for x in f]
        data = parse_input_into_hash_table(without_new_line_chars)
        return count_orbits(data)




def parse_input_into_hash_table(raw_input: List[str]) -> Dict[str, str]:
    result = {}
    separator = ")"
    for line in raw_input:
        center, orbiter = line.split(separator)
        result[orbiter] = center
    return result


def test_get_orbiter_to_center_hash_table():
    assert parse_input_into_hash_table(sample_input_part_one.splitlines()) == {
        "B": "COM",
        "C": "B",
        "D": "C",
        "E": "D",
        "F": "E",
        "G": "B",
        "H": "G",
        "I": "D",
        "J": "E",
        "K": "J",
        "L": "K",
    }


Graph = Dict[str, Set[str]]


def parse_input_into_graph(raw_input: List[str]) -> Graph:
    result: Graph = {}
    separator = ")"
    for line in raw_input:
        center, orbiter = line.split(separator)
        center_data = result[center] if center in result else set()
        orbiter_data = result[orbiter] if orbiter in result else set()
        center_data.add(orbiter)
        orbiter_data.add(center)
        result[orbiter] = orbiter_data
        result[center] = center_data
    return result


sample_input_part_two = """COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L
K)YOU
I)SAN"""


def test_parse_input_into_graph():
    print(parse_input_into_graph(sample_input_part_two.splitlines()))
    assert parse_input_into_graph(sample_input_part_two.splitlines()) == {
        "COM": set(["B"]),
        "B": set(["COM", "G", "C"]),
        "C": set(["B", "D"]),
        "D": set(["C", "E", "I"]),
        "E": set(["D", "F", "J"]),
        "F": set(["E"]),
        "G": set(["B", "H"]),
        "H": set(["G"]),
        "I": set(["D", "SAN"]),
        "J": set(["E", "K"]),
        "K": set(["J", "L", "YOU"]),
        "L": set(["K"]),
        "YOU": set(["K"]),
        "SAN": set(["I"]),
    }


def breadth_first_search_path(graph: Graph, start: str, target: str):
    # Single-ended queue: Add stuff on the right and remove on the left:
    paths = deque([(start, [start])])
    while paths:
        vertex, path = paths.popleft()
        next_vertices = graph[vertex] - set(path)
        for next_vertex in next_vertices:
            if next_vertex == target:
                found_path = path + [next_vertex]
                return found_path
            else:
                paths.append((next_vertex, path + [next_vertex]))


def test_breadth_search_first_path():
    graph = parse_input_into_graph(sample_input_part_two.splitlines())
    assert breadth_first_search_path(graph, "YOU", "SAN") == [
        "YOU",
        "K",
        "J",
        "E",
        "D",
        "I",
        "SAN",
    ]


def part_two():
    with open("day_06_input.txt") as f:
        without_new_line_chars = [x.strip() for x in f]
        graph = parse_input_into_graph(without_new_line_chars)
        shortest_path = breadth_first_search_path(graph, "YOU", "SAN")
        # Minus 3 to account for inclusion of start and end points and that
        # num edges = num nodes - 1:
        return len(shortest_path) - 3

# Note: These tests are commented out because the input and expected output are
# different for each Advent of Code participant. The tests as written below
# pass given my input and the correct output (as judged by the AoC website).
# def test_part_one():
#     assert part_one() == 234446

# def test_part_two():
#     assert part_two() == 385
