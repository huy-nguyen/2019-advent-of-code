from day_04 import int_to_digit_list, has_at_least_two_repeating_digits, has_only_non_decreasing_digits, part_one, get_all_repetition_sequence_lengths, does_satisfy_repetition_requirements_part_two, part_two
from collections import deque


def test_int_to_deque():
    assert int_to_digit_list(278384) == [2, 7, 8, 3, 8, 4]


def test_checkers():
    assert has_at_least_two_repeating_digits(
        int_to_digit_list(111111)
    ) == True
    assert has_only_non_decreasing_digits(
        int_to_digit_list(111111)
    ) == True
    assert has_at_least_two_repeating_digits(
        int_to_digit_list(223450)
    ) == True
    assert has_only_non_decreasing_digits(
        int_to_digit_list(223450)
    ) == False
    assert has_at_least_two_repeating_digits(
        int_to_digit_list(123789)
    ) == False
    assert has_only_non_decreasing_digits(
        int_to_digit_list(123789)
    ) == True


def test_part_one():
    assert part_one() == 921


def test_get_all_reptition_sequences():
    assert get_all_repetition_sequence_lengths(
        int_to_digit_list(112233)
    ) == [2, 2, 2]
    assert get_all_repetition_sequence_lengths(
        int_to_digit_list(123444)
    ) == [3]
    assert get_all_repetition_sequence_lengths(
        int_to_digit_list(111122)
    ) == [4, 2]


def get_has_no_more_than_two_consecutive_identical_digits():
    assert does_satisfy_repetition_requirements_part_two(
        int_to_digit_list(112233)
    ) == True
    assert does_satisfy_repetition_requirements_part_two(
        int_to_digit_list(111122)
    ) == False
    assert does_satisfy_repetition_requirements_part_two(
        int_to_digit_list(123444)
    ) == True


def test_part_two():
    assert part_two() == 603
