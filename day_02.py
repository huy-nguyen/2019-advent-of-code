from typing import List


def execute_program(input: List[int]) -> List[int]:
    should_continue = True
    index = 0
    while(should_continue == True):
        op_code = input[index]
        if(op_code == 1):
            operand1 = input[index + 1]
            operand2 = input[index + 2]
            operand3 = input[index + 3]
            result = input[operand1] + input[operand2]
            input[operand3] = result
            index += 4
        elif(op_code == 2):
            operand1 = input[index + 1]
            operand2 = input[index + 2]
            operand3 = input[index + 3]
            result = input[operand1] * input[operand2]
            input[operand3] = result
            index += 4
        elif (op_code == 99):
            should_continue = False
        else:
            raise RuntimeError("Unknown op code " + str(op_code))
    return input


def parse_input(raw_input: str) -> List[int]:
    input = [int(x) for x in raw_input.split(',')]
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
                if (input_to_try[0] == 19690720):
                    return 100 * noun + verb
        else:
            raise RuntimeError("No noun and verb combination found")
