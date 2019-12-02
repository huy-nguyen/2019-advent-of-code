import math


def get_simple_fuel_for_mass(mass):
    return math.floor(mass / 3) - 2


def part_one():
    with open("day_01_input.txt") as f:
        total = 0
        for line in f:
            mass = float(line)
            total += get_simple_fuel_for_mass(mass)
    return total


def get_complex_fuel_for_mass(input_mass):
    total = 0
    mass = input_mass
    fuel = get_simple_fuel_for_mass(mass)
    while(fuel >= 0):
        total += fuel
        mass = fuel
        fuel = get_simple_fuel_for_mass(mass)
    return total


def part_two():
    with open("day_01_input.txt") as f:
        total = 0
        for line in f:
            mass = float(line)
            total += get_complex_fuel_for_mass(mass)
    return total


assert(round(part_one()) == 3328306)
assert(round(get_complex_fuel_for_mass(14)) == 2)
assert(round(get_complex_fuel_for_mass(1969)) == 966)
assert(round(get_complex_fuel_for_mass(100756)) == 50346)
assert(round(part_two()) == 4989588)
