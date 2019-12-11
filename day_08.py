import itertools
from typing import List
import pytest


def read_into_layers(raw_input: str, width: int, height: int) -> List[List[int]]:
    parsed = [int(x) for x in list(raw_input)]
    all_layers: List[List[int]] = []
    current_layer: List[int] = []
    for value, elem_index in zip(parsed, itertools.cycle(range(width * height))):
        current_layer.append(value)
        if elem_index == width * height - 1:
            all_layers.append(current_layer)
            current_layer = []
    return all_layers


test_image_1 = "123456789012"
test_image_2 = "0222112222120000"


def test_read_into_layers():
    assert read_into_layers(test_image_1, 3, 2) == [
        [1, 2, 3, 4, 5, 6],
        [7, 8, 9, 0, 1, 2]
    ]
    assert read_into_layers(test_image_2, 2, 2) == [
        [0, 2, 2, 2],
        [1, 1, 2, 2],
        [2, 2, 1, 2],
        [0, 0, 0, 0]
    ]


def get_min_zero_layer(raw_input: str, width: int, height: int) -> List[int]:
    layers = read_into_layers(raw_input, width, height)
    min_num_zero_count = float("inf")
    min_num_zero_layer: List[int] = []
    for layer in layers:
        num_zero = layer.count(0)
        if num_zero < min_num_zero_count:
            min_num_zero_count = num_zero
            min_num_zero_layer = layer
    return min_num_zero_layer


def test_get_min_zero_layer():
    assert get_min_zero_layer(test_image_1, 3, 2) == [1, 2, 3, 4, 5, 6]


def part_one():
    with open('day_08_input.txt') as f:
        raw_input = f.readline().strip()
        min_num_zero_digits_layer = get_min_zero_layer(raw_input, 25, 6)
        print(min_num_zero_digits_layer)
        num_1_digits = min_num_zero_digits_layer.count(1)
        num_2_digits = min_num_zero_digits_layer.count(2)
        return num_1_digits * num_2_digits


def test_part_one():
    assert part_one() == 1935


def composite_pixels(pixels: List[int]) -> int:
    transparent_pixel_value = 2
    has_seen_first_non_transparent_pixel = False
    last_pixel = None
    for pixel in pixels:
        if last_pixel is None:
            has_seen_first_non_transparent_pixel = (
                pixel != transparent_pixel_value)
        elif last_pixel == transparent_pixel_value and pixel != transparent_pixel_value:
            has_seen_first_non_transparent_pixel = True
        if has_seen_first_non_transparent_pixel:
            return pixel
        last_pixel = pixel
    # If we haven't seen any non-transparent pixels yet, the result must be a transparent pixel:
    else:
        return transparent_pixel_value


@pytest.mark.parametrize(
    "pixels,expected",
    [
        ([1, 2, 1], 1),
        ([2, 1, 2], 1),
        ([2, 2, 0, 1], 0),
        ([2, 2, 2, 2], 2),
        ([1, 0, 0, 0], 1)
    ]
)
def test_composite_pixels(pixels, expected):
    assert composite_pixels(pixels) == expected


def composite_image(layers: List[List[int]]) -> List[int]:
    result = []
    for pixel_stack in zip(*layers):
        composited_pixel = composite_pixels(pixel_stack)
        result.append(composited_pixel)
    return result


def test_composite_image():
    assert composite_image(read_into_layers(
        test_image_2, 2, 2)) == [0, 1, 1, 0]


def get_graphical_representation(image_pixels: List[int], width: int, height: int):
    rows: List[str] = []
    current_row = ""
    for pixel_value, row_index in zip(image_pixels, itertools.cycle(range(width))):
        graphical_representation = " " if pixel_value == 0 else "X"
        current_row += graphical_representation
        if row_index == width - 1:
            rows.append(current_row)
            current_row = ""
    return rows


def test_get_graphical_reprentation():
    assert get_graphical_representation([0, 1, 1, 0], 2, 2) == [" X", "X "]


def composite_and_display(raw_input: str, width: int, height: int):
    layers = read_into_layers(raw_input, width, height)
    composited = composite_image(layers)
    graphical_representation = get_graphical_representation(
        composited, width, height)
    for row in graphical_representation:
        print(row)


def part_two():
    with open('day_08_input.txt') as f:
        raw_input = f.readline().strip()
        composite_and_display(raw_input, 25, 6)


if __name__ == "__main__":
    part_two()
