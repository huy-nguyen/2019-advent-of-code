from collections import namedtuple
from typing import Tuple, List, Dict
from enum import Enum, unique, auto
import re


@unique
class Op_Code(Enum):
    ADD = auto()
    MULTIPLY = auto()
    INPUT = auto()
    OUTPUT = auto()
    JUMP_IF_TRUE = auto()
    JUMP_IF_FALSE = auto()
    LESS_THAN = auto()
    EQUALS = auto()
    TERMINATE = auto()


@unique
class Mode(Enum):
    POSITION = auto()
    IMMEDIATE = auto()


def str_to_list_digits(input_value: str) -> List[int]:
    list_of_strings: List[str] = list(input_value)
    list_of_digits = [int(x) for x in list_of_strings]
    return list_of_digits


def test_str_to_list_digits():
    assert str_to_list_digits('122345') == [1, 2, 2, 3, 4, 5]


int_to_op_code_and_num_operands: Dict[int, Tuple[Op_Code, int]] = {
    1: (Op_Code.ADD, 3),
    2: (Op_Code.MULTIPLY, 3),
    3: (Op_Code.INPUT, 1),
    4: (Op_Code.OUTPUT, 1),
    5: (Op_Code.JUMP_IF_TRUE, 2),
    6: (Op_Code.JUMP_IF_FALSE, 2),
    7: (Op_Code.LESS_THAN, 3),
    8: (Op_Code.EQUALS, 3),
    99: (Op_Code.TERMINATE, 0),
}

int_to_mode: Dict[int, Mode] = {
    0: Mode.POSITION,
    1: Mode.IMMEDIATE
}
Instruction: Tuple[Op_Code, int, List[Mode]] = namedtuple(
    "Instructions", ['op_code', 'num_operands', 'modes'])

num_digits_in_op_code = 2


def parse_instruction(input_value: int) -> Instruction:
    # Need to ensure that the op code has at least 2 digits b/c otherwise parsing won't work correctly:
    str_input: List[str] = list(f'{input_value:0>{num_digits_in_op_code}}')
    # The last digits are the op code. Whatever that remains are the modes:
    op_code_digits: List[str] = str_input[-num_digits_in_op_code:]
    mode_digits: List[str] = str_input[:len(str_input) - num_digits_in_op_code]

    # Convert 2-digit op code to corresponding enum:
    (op_code, num_operands) = int_to_op_code_and_num_operands[int(
        ''.join(op_code_digits))]

    # Note: modes are originally specified in reverse order:
    unpadded: List[int] = [int(x) for x in reversed(mode_digits)]

    # Make sure # modes match # expected params and fill missing slots with zeros:
    padded = unpadded if num_operands == len(
        unpadded) else unpadded + [0] * (num_operands - len(unpadded))

    modes = [int_to_mode[x] for x in padded]
    return Instruction(op_code=op_code, num_operands=num_operands, modes=modes)


def test_parse_instruction():
    assert parse_instruction(2) == Instruction(Op_Code.MULTIPLY, 3, [
        Mode.POSITION, Mode.POSITION, Mode.POSITION])
    assert parse_instruction(1002) == Instruction(Op_Code.MULTIPLY, 3, [
        Mode.POSITION, Mode.IMMEDIATE, Mode.POSITION])


def read_value_from_buffer(buffer: List[int], operand: int, mode: Mode) -> int:
    if mode == Mode.POSITION:
        return buffer[operand]
    elif mode == Mode.IMMEDIATE:
        return operand
    else:
        raise RuntimeError('Invalid mode ' + str(mode))


def execute_program(raw_input: str):
    buffer = [int(x) for x in raw_input.split(',')]
    index = 0
    should_continue = True
    while(should_continue):
        op_code, num_operands, modes = parse_instruction(buffer[index])
        if op_code == Op_Code.ADD:
            operand_1 = read_value_from_buffer(
                buffer, buffer[index + 1], modes[0])
            operand_2 = read_value_from_buffer(
                buffer, buffer[index + 2], modes[1])
            operand_3 = buffer[index + 3]
            result = operand_1 + operand_2
            buffer[operand_3] = result
            index += num_operands + 1
        elif op_code == Op_Code.MULTIPLY:
            operand_1 = read_value_from_buffer(
                buffer, buffer[index + 1], modes[0])
            operand_2 = read_value_from_buffer(
                buffer, buffer[index + 2], modes[1])
            operand_3 = buffer[index + 3]
            result = operand_1 * operand_2
            buffer[operand_3] = result
            index += num_operands + 1
        elif op_code == Op_Code.INPUT:
            operand = buffer[index + 1]
            result = int(input('Enter a value: '))
            buffer[operand] = result
            index += num_operands + 1
        elif op_code == Op_Code.OUTPUT:
            operand = read_value_from_buffer(
                buffer, buffer[index + 1], modes[0])
            index += num_operands + 1
            print(operand)
        elif op_code == Op_Code.JUMP_IF_TRUE:
            operand_1 = read_value_from_buffer(
                buffer, buffer[index + 1], modes[0])
            operand_2 = read_value_from_buffer(
                buffer, buffer[index + 2], modes[1])
            if operand_1 is not 0:
                index = operand_2
            else:
                index += num_operands + 1
        elif op_code == Op_Code.JUMP_IF_FALSE:
            operand_1 = read_value_from_buffer(
                buffer, buffer[index + 1], modes[0])
            operand_2 = read_value_from_buffer(
                buffer, buffer[index + 2], modes[1])
            if operand_1 is 0:
                index = operand_2
            else:
                index += num_operands + 1
        elif op_code == Op_Code.LESS_THAN:
            operand_1 = read_value_from_buffer(
                buffer, buffer[index + 1], modes[0])
            operand_2 = read_value_from_buffer(
                buffer, buffer[index + 2], modes[1])
            operand_3 = buffer[index + 3]
            if operand_1 < operand_2:
                buffer[operand_3] = 1
            else:
                buffer[operand_3] = 0
            index += num_operands + 1
        elif op_code == Op_Code.EQUALS:
            operand_1 = read_value_from_buffer(
                buffer, buffer[index + 1], modes[0])
            operand_2 = read_value_from_buffer(
                buffer, buffer[index + 2], modes[1])
            operand_3 = buffer[index + 3]
            if operand_1 == operand_2:
                buffer[operand_3] = 1
            else:
                buffer[operand_3] = 0
            index += num_operands + 1
        elif op_code == Op_Code.TERMINATE:
            should_continue = False
            index += num_operands + 1
            break
    return buffer


def test_simple_programs():
    # Tests from day 2:
    assert execute_program('1,9,10,3,2,3,11,0,99,30,40,50') == [
        3500, 9, 10, 70, 2, 3, 11, 0, 99, 30, 40, 50]
    assert execute_program('1,0,0,0,99') == [2, 0, 0, 0, 99]
    assert execute_program('2,3,0,3,99') == [2, 3, 0, 6, 99]
    assert execute_program('2,4,4,5,99,0') == [
        2, 4, 4, 5, 99, 9801]
    assert execute_program('1,1,1,4,99,5,6,0,99') == [
        30, 1, 1, 4, 2, 5, 6, 0, 99]
    # Tests from day 5 part 1:
    assert execute_program('1002,4,3,4,33') == [1002, 4, 3, 4, 99]
    assert execute_program('1101,100,-1,4,0') == [1101, 100, -1, 4, 99]


def execute_day_05_input():
    with open('day_05_input.txt') as f:
        raw_input = f.readline()
        execute_program(raw_input)


def test_part_one(monkeypatch, capfd):
    monkeypatch.setattr('builtins.input', lambda _: "1")
    execute_day_05_input()
    out, _ = capfd.readouterr()
    assert re.match(r'(0\n)+4601506', out) is not None


def test_part_two(monkeypatch, capfd):
    monkeypatch.setattr('builtins.input', lambda _: "5")
    execute_day_05_input()
    out, _ = capfd.readouterr()
    assert re.match(r'5525561', out) is not None


equal_op_code_position_mode_program = '3,9,8,9,10,9,4,9,99,-1,8'


def test_equal_op_code_true_position(monkeypatch, capfd):
    monkeypatch.setattr('builtins.input', lambda _: "8")
    execute_program(equal_op_code_position_mode_program)
    out, _ = capfd.readouterr()
    assert re.match(r'\s*1\s*', out)


def test_equal_op_code_false_position(monkeypatch, capfd):
    monkeypatch.setattr('builtins.input', lambda _: "13")
    execute_program(equal_op_code_position_mode_program)
    out, _ = capfd.readouterr()
    assert re.match(r'\s*0\s*', out)


less_than_op_code_position_mode_program = '3,9,7,9,10,9,4,9,99,-1,8'


def test_less_than_op_code_true_position(monkeypatch, capfd):
    monkeypatch.setattr('builtins.input', lambda _: "5")
    execute_program(less_than_op_code_position_mode_program)
    out, _ = capfd.readouterr()
    assert re.match(r'\s*1\s*', out)


def test_less_than_op_code_false_position(monkeypatch, capfd):
    monkeypatch.setattr('builtins.input', lambda _: "13")
    execute_program(less_than_op_code_position_mode_program)
    out, _ = capfd.readouterr()
    assert re.match(r'\s*0\s*', out)


equal_op_code_immediate_mode_program = '3,3,1108,-1,8,3,4,3,99'


def test_equal_op_code_true_immediate(monkeypatch, capfd):
    monkeypatch.setattr('builtins.input', lambda _: "8")
    execute_program(equal_op_code_immediate_mode_program)
    out, _ = capfd.readouterr()
    assert re.match(r'\s*1\s*', out)


def test_equal_op_code_false_immediate(monkeypatch, capfd):
    monkeypatch.setattr('builtins.input', lambda _: "13")
    execute_program(equal_op_code_immediate_mode_program)
    out, _ = capfd.readouterr()
    assert re.match(r'\s*0\s*', out)


less_than_op_code_immediate_mode_program = '3,3,1107,-1,8,3,4,3,99'


def test_less_than_op_code_true_immediate(monkeypatch, capfd):
    monkeypatch.setattr('builtins.input', lambda _: "5")
    execute_program(less_than_op_code_immediate_mode_program)
    out, _ = capfd.readouterr()
    assert re.match(r'\s*1\s*', out)


def test_less_than_op_code_false_immediate(monkeypatch, capfd):
    monkeypatch.setattr('builtins.input', lambda _: "13")
    execute_program(less_than_op_code_immediate_mode_program)
    out, _ = capfd.readouterr()
    assert re.match(r'\s*0\s*', out)


jump_op_code_position_mode_program = '3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9'


def test_jump_op_code_zero_input_position(monkeypatch, capfd):
    monkeypatch.setattr('builtins.input', lambda _: "0")
    execute_program(jump_op_code_position_mode_program)
    out, _ = capfd.readouterr()
    assert re.match(r'\s*0\s*', out)


def test_jump_op_code_non_zero_input_position(monkeypatch, capfd):
    monkeypatch.setattr('builtins.input', lambda _: "100")
    execute_program(jump_op_code_position_mode_program)
    out, _ = capfd.readouterr()
    assert re.match(r'\s*1\s*', out)


jump_op_code_immediate_mode_program = '3,3,1105,-1,9,1101,0,0,12,4,12,99,1'


def test_jump_op_code_zero_input_immediate(monkeypatch, capfd):
    monkeypatch.setattr('builtins.input', lambda _: "0")
    execute_program(jump_op_code_immediate_mode_program)
    out, _ = capfd.readouterr()
    assert re.match(r'\s*0\s*', out)


def test_jump_op_code_non_zero_input_immediate(monkeypatch, capfd):
    monkeypatch.setattr('builtins.input', lambda _: "100")
    execute_program(jump_op_code_immediate_mode_program)
    out, _ = capfd.readouterr()
    assert re.match(r'\s*1\s*', out)


large_program = '3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99'


def test_large_program_below_8(monkeypatch, capfd):
    monkeypatch.setattr('builtins.input', lambda _: "7")
    execute_program(large_program)
    out, _ = capfd.readouterr()
    assert re.match(r'\s*999\s*', out)


def test_large_program_exactly_8(monkeypatch, capfd):
    monkeypatch.setattr('builtins.input', lambda _: "8")
    execute_program(large_program)
    out, _ = capfd.readouterr()
    assert re.match(r'\s*1000\s*', out)


def test_large_program_above_8(monkeypatch, capfd):
    monkeypatch.setattr('builtins.input', lambda _: "9")
    execute_program(large_program)
    out, _ = capfd.readouterr()
    assert re.match(r'\s*1001\s*', out)


if __name__ == "__main__":
    execute_day_05_input()
