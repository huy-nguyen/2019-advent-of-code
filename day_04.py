from typing import List, MutableSequence, Dict, Union
from collections import deque


def int_to_digit_list(input: int) -> List[int]:
    list_of_strings: List[str] = list(str(input))
    list_of_ints = [int(x) for x in list_of_strings]
    return list_of_ints


def has_at_least_two_repeating_digits(input: List[int]) -> bool:
    unique_digits = set(input)
    return len(unique_digits) <= len(input) - 1


def has_non_decreasing_digits(input: List[int]) -> bool:
    for a, b in zip(input[:-1], input[1:]):
        if a > b:
            return False
    return True


def get_all_numbers_between_bounds_part_one(lower_bound: int, upper_bound: int):
    all_numbers_in_range: List[List[int]] = [
        int_to_digit_list(x) for x in range(lower_bound, upper_bound + 1)
    ]
    numbers = [
        x for x in all_numbers_in_range
        if has_at_least_two_repeating_digits(x) == True and
        has_non_decreasing_digits(x)
    ]
    return len(numbers)


def part_one():
    return get_all_numbers_between_bounds_part_one(278384, 824795)


def get_all_repetition_sequences(input: List[int]):
    last_digit = None
    current_sequence_length = 0
    all_sequence_lengths: List[int] = []
    is_inside_sequence = False
    for digit in input:
        if digit == last_digit:
            current_sequence_length += 1
            is_inside_sequence = True
        else:
            if is_inside_sequence:
                current_sequence_length += 1
                all_sequence_lengths.append(current_sequence_length)
                current_sequence_length = 0
            is_inside_sequence = False
        last_digit = digit

    if current_sequence_length > 0:
        current_sequence_length += 1
        all_sequence_lengths.append(current_sequence_length)
    return all_sequence_lengths


def has_no_more_than_two_consecutive_identical_digits(input: List[int]):
    repetition_sequences = get_all_repetition_sequences(input)
    return len(repetition_sequences) > 0 and 2 in repetition_sequences


def get_all_numbers_between_bounds_part_two(lower_bound: int, upper_bound: int):
    all_numbers_in_range: List[List[int]] = [
        int_to_digit_list(x) for x in range(lower_bound, upper_bound + 1)
    ]
    numbers = [
        x for x in all_numbers_in_range
        if has_no_more_than_two_consecutive_identical_digits(x) == True and
        has_non_decreasing_digits(x)
    ]
    return len(numbers)


def part_two():
    return get_all_numbers_between_bounds_part_two(278384, 824795)
