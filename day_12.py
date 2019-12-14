import copy
from math import gcd
from functools import reduce
from typing import Tuple, List
from collections import namedtuple
from dataclasses import dataclass, asdict, astuple, replace
import itertools


@dataclass
class Position:
    x: int
    y: int
    z: int


@dataclass
class Velocity:
    x: int = 0
    y: int = 0
    z: int = 0


@dataclass
class Moon:
    name: str
    position: Position
    velocity: Velocity


def apply_gravity_two_moons(a: Moon, b: Moon):
    for (a_position_component, b_position_component, (component_name, prev_a_velocity_component), prev_b_velocity_component) in zip(
        astuple(a.position),
        astuple(b.position),
        asdict(a.velocity).items(),
        asdict(b.velocity).values()
    ):
        if a_position_component != b_position_component:
            if a_position_component * b_position_component < 0:
                # This means a and b are on opposite sides of the origin:
                positive_moon, negative_moon, positive_moon_velocity_component, negative_moon_velocity_component = (
                    a, b, prev_a_velocity_component, prev_b_velocity_component
                ) if a_position_component > 0 else (
                    b, a, prev_b_velocity_component, prev_a_velocity_component
                )
                positive_moon.velocity = replace(
                    positive_moon.velocity, **{component_name: positive_moon_velocity_component - 1})
                negative_moon.velocity = replace(
                    negative_moon.velocity, **{component_name: negative_moon_velocity_component + 1})
            elif a_position_component * b_position_component > 0:
                # This means a and b are on the same side of the origin:
                further_moon, closer_moon, further_moon_velocity_component, closer_moon_velocity_component = (
                    a, b, prev_a_velocity_component, prev_b_velocity_component,
                ) if abs(a_position_component) > abs(b_position_component) else (
                    b, a, prev_b_velocity_component, prev_a_velocity_component,
                )
                # This is the change in velocity to bring the further-away moon closer to the origin:
                velocity_change_further_moon = 1 if a_position_component < 0 else -1

                further_moon.velocity = replace(further_moon.velocity, **{
                                                component_name: further_moon_velocity_component + velocity_change_further_moon})
                closer_moon.velocity = replace(closer_moon.velocity, **{
                                               component_name: closer_moon_velocity_component - velocity_change_further_moon})
            else:
                # This means either a or b is on the origin:
                zero_moon, non_zero_moon, zero_moon_velocity_component, non_zero_moon_velocity_component, non_zero_moon_position_component = (
                    a, b, prev_a_velocity_component, prev_b_velocity_component, b_position_component,
                ) if a_position_component == 0 else (
                    b, a, prev_b_velocity_component, prev_a_velocity_component, a_position_component
                )
                velocity_change_non_zero_moon = 1 if non_zero_moon_position_component < 0 else -1
                non_zero_moon.velocity = replace(non_zero_moon.velocity, **{
                                                 component_name: non_zero_moon_velocity_component + velocity_change_non_zero_moon})
                zero_moon.velocity = replace(
                    zero_moon.velocity, **{component_name: zero_moon_velocity_component - velocity_change_non_zero_moon})


def test_apply_gravity_two_moons():
    a = Moon(name="A", position=Position(x=-1, y=0, z=2), velocity=Velocity())
    b = Moon(name="B", position=Position(
        x=2, y=-10, z=-7), velocity=Velocity())
    apply_gravity_two_moons(a, b)
    assert a == Moon(
        name="A", position=Position(x=-1, y=0, z=2),
        velocity=Velocity(x=1, y=-1, z=-1)
    )
    assert b == Moon(
        name="B", position=Position(x=2, y=-10, z=-7),
        velocity=Velocity(x=-1, y=1, z=1)
    )


def move_moon_according_to_velocity(moon: Moon):
    for velocity_component, (component_name, position_component) in zip(
        astuple(moon.velocity),
        asdict(moon.position).items()
    ):
        new_position_component = position_component + velocity_component
        moon.position = replace(
            moon.position, **{component_name: new_position_component})


def test_move_moon_according_to_velocity():
    a = Moon(
        name="A", position=Position(x=-1, y=0, z=2),
        velocity=Velocity(x=1, y=-1, z=-1)
    )
    move_moon_according_to_velocity(a)
    assert a == Moon(
        name="A", position=Position(x=0, y=-1, z=1),
        velocity=Velocity(x=1, y=-1, z=-1)
    )


def perform_one_pass(moons: List[Moon]):
    for moon_a, moon_b in itertools.combinations(moons, 2):
        apply_gravity_two_moons(moon_a, moon_b)

    for moon in moons:
        move_moon_according_to_velocity(moon)

    return moons


def test_perform_one_pass_1():
    a = Moon(name="A", position=Position(x=-1, y=0, z=2), velocity=Velocity())
    b = Moon(name="B", position=Position(
        x=2, y=-10, z=-7), velocity=Velocity())
    c = Moon(name="C", position=Position(x=4, y=-8, z=8), velocity=Velocity())
    d = Moon(name="D", position=Position(x=3, y=5, z=-1), velocity=Velocity())
    moons = [a, b, c, d]

    perform_one_pass(moons)
    assert a == Moon(
        name="A",
        position=Position(x=2, y=-1, z=1),
        velocity=Velocity(x=3, y=-1, z=-1)
    )
    assert b == Moon(
        name="B",
        position=Position(x=3, y=-7, z=-4),
        velocity=Velocity(x=1, y=3, z=3)
    )
    assert c == Moon(
        name="C",
        position=Position(x=1, y=-7, z=5),
        velocity=Velocity(x=-3, y=1, z=-3)
    )
    assert d == Moon(
        name="D",
        position=Position(x=2, y=2, z=0),
        velocity=Velocity(x=-1, y=-3, z=1)
    )

    for _ in range(9):
        perform_one_pass(moons)

    assert a == Moon(
        name="A",
        position=Position(x=2, y=1, z=-3),
        velocity=Velocity(x=-3, y=-2, z=1)
    )
    assert b == Moon(
        name="B",
        position=Position(x=1, y=-8, z=0),
        velocity=Velocity(x=-1, y=1, z=3)
    )
    assert c == Moon(
        name="C",
        position=Position(x=3, y=-6, z=1),
        velocity=Velocity(x=3, y=2, z=-3)
    )
    assert d == Moon(
        name="D",
        position=Position(x=2, y=0, z=4),
        velocity=Velocity(x=1, y=-1, z=-1)
    )


def get_total_energy(moon: Moon) -> int:
    position = moon.position
    velocity = moon.velocity
    potential_energy = abs(position.x) + abs(position.y) + abs(position.z)
    kinetic_energy = abs(velocity.x) + abs(velocity.y) + abs(velocity.z)
    return potential_energy * kinetic_energy


def get_total_energy_system(moons: List[Moon]) -> int:
    return sum([get_total_energy(moon) for moon in moons])


def test_energy():
    a = Moon(
        name="A",
        position=Position(x=2, y=1, z=-3),
        velocity=Velocity(x=-3, y=-2, z=1)
    )
    b = Moon(
        name="B",
        position=Position(x=1, y=-8, z=0),
        velocity=Velocity(x=-1, y=1, z=3)
    )
    c = Moon(
        name="C",
        position=Position(x=3, y=-6, z=1),
        velocity=Velocity(x=3, y=2, z=-3)
    )
    d = Moon(
        name="D",
        position=Position(x=2, y=0, z=4),
        velocity=Velocity(x=1, y=-1, z=-1)
    )
    assert get_total_energy(a) == 36
    assert get_total_energy(b) == 45
    assert get_total_energy(c) == 80
    assert get_total_energy(d) == 18
    assert get_total_energy_system([a, b, c, d]) == 179


def test_perform_one_pass_2():
    a = Moon(name="A", position=Position(
        x=-8, y=-10, z=0), velocity=Velocity())
    b = Moon(name="B", position=Position(x=5, y=5, z=10), velocity=Velocity())
    c = Moon(name="C", position=Position(x=2, y=-7, z=3), velocity=Velocity())
    d = Moon(name="D", position=Position(x=9, y=-8, z=-3), velocity=Velocity())
    moons = [a, b, c, d]

    for _ in range(100):
        perform_one_pass(moons)

    assert a == Moon(
        name="A",
        position=Position(x=8, y=-12, z=-9),
        velocity=Velocity(x=-7, y=3, z=0)
    )
    assert b == Moon(
        name="B",
        position=Position(x=13, y=16, z=-3),
        velocity=Velocity(x=3, y=-11, z=-5)
    )
    assert c == Moon(
        name="C",
        position=Position(x=-29, y=-11, z=-1),
        velocity=Velocity(x=-3, y=7, z=4)
    )
    assert d == Moon(
        name="D",
        position=Position(x=16, y=-13, z=23),
        velocity=Velocity(x=7, y=1, z=1)
    )
    assert get_total_energy_system(moons) == 1940


def get_day_12_input():
    return [
        Moon(
            name="A",
            position=Position(x=16, y=-11, z=2),
            velocity=Velocity()
        ),
        Moon(
            name="B",
            position=Position(x=0, y=-4, z=7),
            velocity=Velocity()
        ),
        Moon(
            name="C",
            position=Position(x=6, y=4, z=-10),
            velocity=Velocity()
        ),
        Moon(
            name="D",
            position=Position(x=-3, y=-2, z=-4),
            velocity=Velocity()
        ),
    ]


def part_one():
    moons = get_day_12_input()
    for _ in range(1000):
        perform_one_pass(moons)

    return get_total_energy_system(moons)


def lcm(denominators):
    return reduce(lambda a, b: a*b // gcd(a, b), denominators)


def test_part_one():
    assert part_one() == 10055


def shallow_copy_moons(moons: List[Moon]) -> List[Moon]:
    return [copy.copy(moon) for moon in moons]


def get_cycle_period(moons):
    initial_positions = [moon.position for moon in moons]

    period_x = 0
    moons_x = shallow_copy_moons(moons)
    while True:
        period_x += 1
        perform_one_pass(moons_x)
        for moon, initial_position in zip(moons_x, initial_positions):
            if moon.position.x != initial_position.x or moon.velocity.x != 0:
                break
        else:
            break

    period_y = 0
    moons_y = shallow_copy_moons(moons)
    while True:
        period_y += 1
        perform_one_pass(moons_y)
        for moon, initial_position in zip(moons_y, initial_positions):
            if moon.position.y != initial_position.y or moon.velocity.y != 0:
                break
        else:
            break
    period_z = 0
    moons_z = shallow_copy_moons(moons)
    while True:
        period_z += 1
        perform_one_pass(moons_z)
        for moon, initial_position in zip(moons_z, initial_positions):
            if moon.position.z != initial_position.z or moon.velocity.z != 0:
                break
        else:
            break
    return lcm([period_x, period_y, period_z])


def test_get_cycle_period():
    assert get_cycle_period([
        Moon(name="A", position=Position(x=-1, y=0, z=2), velocity=Velocity()),
        Moon(name="B", position=Position(x=2, y=-10, z=-7), velocity=Velocity()),
        Moon(name="C", position=Position(x=4, y=-8, z=8), velocity=Velocity()),
        Moon(name="D", position=Position(x=3, y=5, z=-1), velocity=Velocity()),
    ]) == 2772
    assert get_cycle_period([
        Moon(name="A", position=Position(x=-8, y=-10, z=0), velocity=Velocity()),
        Moon(name="B", position=Position(x=5, y=5, z=10), velocity=Velocity()),
        Moon(name="C", position=Position(x=2, y=-7, z=3), velocity=Velocity()),
        Moon(name="D", position=Position(x=9, y=-8, z=-3), velocity=Velocity()),
    ]) == 4686774924


def test_part_two():
    assert get_cycle_period(get_day_12_input()) == 374307970285176


if __name__ == "__main__":
    pass
