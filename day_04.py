from typing import List, MutableSequence, Dict, Union
from collections import deque


def int_to_digit_list(input: int) -> List[int]:
    list_of_strings: List[str] = list(str(input))
    list_of_ints = [int(x) for x in list_of_strings]
    return list_of_ints


def get_all_repetition_sequence_lengths(input: List[int]) -> List[int]:
    prev_digit = None
    current_sequence_length = 0
    all_sequence_lengths: List[int] = []
    is_inside_sequence = False
    for current_digit in input:
        if current_digit == prev_digit:
            current_sequence_length += 1
            is_inside_sequence = True
        else:
            if is_inside_sequence:
                current_sequence_length += 1
                all_sequence_lengths.append(current_sequence_length)
                current_sequence_length = 0
            is_inside_sequence = False
        prev_digit = current_digit

    if current_sequence_length > 0:
        current_sequence_length += 1
        all_sequence_lengths.append(current_sequence_length)
    return all_sequence_lengths


def has_at_least_two_repeating_digits(input: List[int]) -> bool:
    repetition_sequence_lengths = get_all_repetition_sequence_lengths(input)
    repetition_sequence_longer_than_2: List[bool] = [
        x >= 2 for x in repetition_sequence_lengths]
    return len(repetition_sequence_longer_than_2) > 0 and any(repetition_sequence_longer_than_2)


def has_only_non_decreasing_digits(input: List[int]) -> bool:
    for a, b in zip(input[:-1], input[1:]):
        if a > b:
            return False
    return True


def count_eliglble_numbers_between_bounds_part_one(lower_bound: int, upper_bound: int) -> int:
    all_numbers_in_range: List[List[int]] = [
        int_to_digit_list(x) for x in range(lower_bound, upper_bound + 1)
    ]
    eligible_numbers = [
        x for x in all_numbers_in_range
        if has_at_least_two_repeating_digits(x) == True and
        has_only_non_decreasing_digits(x) == True
    ]
    return len(eligible_numbers)


def part_one():
    return count_eliglble_numbers_between_bounds_part_one(278384, 824795)


def does_satisfy_repetition_requirements_part_two(input: List[int]):
    repetition_sequence_lengths = get_all_repetition_sequence_lengths(input)
    return len(repetition_sequence_lengths) > 0 and 2 in repetition_sequence_lengths


def count_eligible_numbers_between_bounds_part_two(lower_bound: int, upper_bound: int):
    all_numbers_in_range: List[List[int]] = [
        int_to_digit_list(x) for x in range(lower_bound, upper_bound + 1)
    ]
    numbers = [
        x for x in all_numbers_in_range
        if does_satisfy_repetition_requirements_part_two(x) == True and
        has_only_non_decreasing_digits(x) == True
    ]
    return len(numbers)


def part_two():
    return count_eligible_numbers_between_bounds_part_two(278384, 824795)
