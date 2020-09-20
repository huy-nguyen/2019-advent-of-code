from typing import List


def execute_program(input: List[int]) -> List[int]:
    should_continue = True
    index = 0
    while should_continue == True:
        op_code = input[index]
        if op_code == 1:
            operand1 = input[index + 1]
            operand2 = input[index + 2]
            operand3 = input[index + 3]
            result = input[operand1] + input[operand2]
            input[operand3] = result
            index += 4
        elif op_code == 2:
            operand1 = input[index + 1]
            operand2 = input[index + 2]
            operand3 = input[index + 3]
            result = input[operand1] * input[operand2]
            input[operand3] = result
            index += 4
        elif op_code == 99:
            should_continue = False
        else:
            raise RuntimeError("Unknown op code " + str(op_code))
    return input


def test_execute_program():
    assert execute_program(parse_input("1,9,10,3,2,3,11,0,99,30,40,50")) == [
        3500,
        9,
        10,
        70,
        2,
        3,
        11,
        0,
        99,
        30,
        40,
        50,
    ]
    assert execute_program(parse_input("1,0,0,0,99")) == [2, 0, 0, 0, 99]
    assert execute_program(parse_input("2,3,0,3,99")) == [2, 3, 0, 6, 99]
    assert execute_program(parse_input("2,4,4,5,99,0")) == [2, 4, 4, 5, 99, 9801]
    assert execute_program(parse_input("1,1,1,4,99,5,6,0,99")) == [
        30,
        1,
        1,
        4,
        2,
        5,
        6,
        0,
        99,
    ]


def parse_input(raw_input: str) -> List[int]:
    input = [int(x) for x in raw_input.split(",")]
    return input


def part_one():
    with open("day_02_input.txt") as f:
        raw_input = f.readline()
        parsed_input = parse_input(raw_input)
        parsed_input[1] = 12
        parsed_input[2] = 2
        return execute_program(parsed_input)




def part_two():
    with open("day_02_input.txt") as f:
        raw_input = f.readline()
        parsed_input = parse_input(raw_input)
        for noun in range(100):
            for verb in range(100):
                input_to_try = parsed_input.copy()
                input_to_try[1] = noun
                input_to_try[2] = verb
                execute_program(input_to_try)
                if input_to_try[0] == 19690720:
                    return 100 * noun + verb
        else:
            raise RuntimeError("No noun and verb combination found")


# Note: These tests are commented out because the input and expected output are
# different for each Advent of Code participant. The tests as written below
# pass given my input and the correct output (as judged by the AoC website).
# def test_part_one():
#     assert part_one()[0] == 4090689
# def test_part_two():
#     assert part_two() == 7733
