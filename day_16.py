import numpy as np
from more_itertools import take
import pytest
from typing import List

base_pattern = [0, 1, 0, -1]


def get_pattern_digit(output_elem_index: int, index: int) -> int:
    # How many instances of each digit are generated per one cycle of going through [0, 1, 0, -1]:
    normal_repetition_count_for_each_digit = output_elem_index + 1
    # How many digits we would have to generate to get out of the "initial cycle" where we have to skip one
    # instance of 0:
    normal_cycle_length = 4 * normal_repetition_count_for_each_digit
    initial_cycle_length = normal_cycle_length - 1
    if index < initial_cycle_length:
        if index < normal_repetition_count_for_each_digit - 1:
            return 0
        elif index < 2 * normal_repetition_count_for_each_digit - 1:
            return 1
        elif index < 3 * normal_repetition_count_for_each_digit - 1:
            return 0
        else:
            return -1
    else:
        index = (index - initial_cycle_length) % normal_cycle_length
        quotient = index // normal_repetition_count_for_each_digit
        return base_pattern[quotient]


@pytest.mark.parametrize(
    "output_elem_index,expected",
    [
        (0, [1, 0, -1, 0, 1, 0, -1, 0]),
        (1, [0, 1, 1, 0, 0, -1, -1, 0]),
        (2, [0, 0, 1, 1, 1, 0, 0, 0]),
        (3, [0, 0, 0, 1, 1, 1, 1, 0]),
        (4, [0, 0, 0, 0, 1, 1, 1, 1]),
        (5, [0, 0, 0, 0, 0, 1, 1, 1]),
        (6, [0, 0, 0, 0, 0, 0, 1, 1]),
        (7, [0, 0, 0, 0, 0, 0, 0, 1]),
    ],
)
def test_get_pattern_digit_no_skip(output_elem_index, expected):
    actual = [get_pattern_digit(output_elem_index, i) for i in range(8)]
    assert actual == expected


@pytest.mark.parametrize(
    "output_elem_index,skip_count,comparison_size,expected",
    [
        (0, 1, 7, [0, -1, 0, 1, 0, -1, 0]),
        (0, 2, 6, [-1, 0, 1, 0, -1, 0]),
        (0, 3, 5, [0, 1, 0, -1, 0]),
        (0, 4, 4, [1, 0, -1, 0]),
        (3, 1, 7, [0, 0, 1, 1, 1, 1, 0]),
    ],
)
def test_get_pattern_digit_with_skip(
    output_elem_index: int, skip_count: int, comparison_size: int, expected: List[int]
):
    actual = [get_pattern_digit(output_elem_index, i) for i in range(skip_count, 8)]
    assert actual == expected


def perform_n_phases(
    string_input: str, num_phases: int, base_pattern_skip_count: int
) -> str:
    val = np.array([int(char) for char in string_input])
    pattern_cache = {}
    input_signal_length = len(val)
    for i in range(num_phases):
        print("phase", i)
        next_val = np.empty(input_signal_length, dtype=int)
        for output_elem_index in range(input_signal_length):
            if output_elem_index in pattern_cache:
                pattern = pattern_cache[output_elem_index]
            else:
                pattern = [
                    get_pattern_digit(
                        output_elem_index=output_elem_index + base_pattern_skip_count,
                        index=x,
                    )
                    for x in range(
                        base_pattern_skip_count,
                        base_pattern_skip_count + input_signal_length,
                    )
                ]
                pattern = np.array(pattern)
                pattern_cache[output_elem_index] = pattern
            dot_product = np.dot(val, pattern)
            next_val[output_elem_index] = abs(dot_product) % 10
        val = next_val
    return "".join([str(x) for x in val.tolist()])


@pytest.mark.parametrize(
    "string_input,num_phases,expected",
    [
        ("12345678", 1, "48226158"),
        ("12345678", 2, "34040438"),
        ("12345678", 3, "03415518"),
        ("12345678", 4, "01029498"),
    ],
)
def test_perform_n_phases_small_num_phases(string_input, num_phases, expected):
    actual = perform_n_phases(string_input, num_phases, 0)
    assert actual == expected


@pytest.mark.parametrize(
    "input_string,num_phases,expected_first_eight",
    [
        ("80871224585914546619083218645595", 100, "24176176"),
        ("19617804207202209144916044189917", 100, "73745418"),
        ("69317163492948606335995924319873", 100, "52432133"),
    ],
)
def test_perform_n_phases_large_num_phases(
    input_string: str, num_phases: int, expected_first_eight: str
):
    actual = perform_n_phases(input_string, num_phases, 0)
    assert actual[:8] == expected_first_eight


def part_one():
    with open("day_16_input.txt") as f:
        text = next(f)[:-1]
        output = perform_n_phases(text, 100, base_pattern_skip_count=0)
        return output[:8]


# Note: commented out because the input and expected output are different for each participant:
# def test_part_one():
#     expected = "70856418"
#     assert part_one() == expected


def perform_n_phases_with_input_repetition_and_offset(
    string_input: str, num_phases: int, input_repetition_count: int
) -> str:
    offset = int(string_input[:7])
    fully_repeated_string_input = string_input * input_repetition_count
    truncated_string_input = fully_repeated_string_input[offset:]

    result = perform_n_phases(
        string_input=truncated_string_input,
        num_phases=num_phases,
        base_pattern_skip_count=offset,
    )
    return result[:8]


def perform_n_phases_large_offset(
    unrepeated_string_input: str, input_repetition_count: int, num_phases: int
) -> str:
    unrepeated_list_of_ints = [int(char) for char in unrepeated_string_input]
    offset = int(unrepeated_string_input[:7])
    unrepeated_input_length = len(unrepeated_list_of_ints)
    assert offset > (unrepeated_input_length * input_repetition_count) / 2
    val = (unrepeated_list_of_ints * input_repetition_count)[offset:]
    output_length = len(val)
    for _ in range(num_phases):
        new_val = [0] * output_length
        summed = 0
        for j in range(len(val) - 1, -1, -1):
            summed += val[j]
            new_val[j] = summed % 10
        val = new_val
    return "".join([str(x) for x in val[:8]])


@pytest.mark.parametrize(
    "unrepeated_string_input,expected",
    [
        ("03036732577212944063491565474664", "84462026"),
        ("02935109699940807407585447034323", "78725270"),
        ("03081770884921959731165446850517", "53553731"),
    ],
)
def test_perform_n_phases_large_offset(unrepeated_string_input, expected):
    assert (
        perform_n_phases_large_offset(
            unrepeated_string_input=unrepeated_string_input,
            input_repetition_count=10000,
            num_phases=100,
        )
        == expected
    )


def part_two():
    with open("day_16_input.txt") as f:
        text = next(f)[:-1]
        return perform_n_phases_large_offset(
            unrepeated_string_input=text,
            input_repetition_count=10000,
            num_phases=100,
        )


# Note: commented out because the input and expected output are different for each participant:
# def test_part_two():
#     expected = "87766336"
#     assert part_two() == expected
