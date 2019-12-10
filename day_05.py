from collections import namedtuple
from typing import Tuple, List, Dict
from enum import Enum, unique, auto
import re
from unittest.mock import Mock, call, AsyncMock
import pytest


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


def get_input_generator(prompt: str):
    while(True):
        value = input(prompt)
        yield value

def async_builtin_input(prompt: str):
    return input(prompt)


@unique
class MessageType(Enum):
    GET_INPUT = auto()
    PRINT_OUTPUT = auto()
    TERMINATE = auto()

ProgramMessage = namedtuple("ProgramMessage", ["type", "arg"])

def compile_source_code(source_code: str):
    """Last two arguments are used for mocking in tests and also for use in day 7.
    get_user_input is an awaitable.
    """
    buffer = [int(x) for x in source_code.split(',')]
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
            input_from_user = yield ProgramMessage(type=MessageType.GET_INPUT, arg="Enter a number: ")
            result = int(input_from_user)
            buffer[operand] = result
            index += num_operands + 1
        elif op_code == Op_Code.OUTPUT:
            operand = read_value_from_buffer(
                buffer, buffer[index + 1], modes[0])
            index += num_operands + 1
            yield ProgramMessage(type=MessageType.PRINT_OUTPUT, arg=operand)
        elif op_code == Op_Code.JUMP_IF_TRUE:
            operand_1 = read_value_from_buffer(
                buffer, buffer[index + 1], modes[0])
            operand_2 = read_value_from_buffer(
                buffer, buffer[index + 2], modes[1])
            if operand_1 != 0:
                index = operand_2
            else:
                index += num_operands + 1
        elif op_code == Op_Code.JUMP_IF_FALSE:
            operand_1 = read_value_from_buffer(
                buffer, buffer[index + 1], modes[0])
            operand_2 = read_value_from_buffer(
                buffer, buffer[index + 2], modes[1])
            if operand_1 == 0:
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
            yield ProgramMessage(type=MessageType.TERMINATE, arg=buffer)

def run_with_input_output(source_code, get_user_input, print_output):
    program = compile_source_code(source_code)
    should_continue = True
    final_output = None
    try:
        message = next(program)
        while should_continue:
            if message.type == MessageType.GET_INPUT:
                user_input = get_user_input(message.arg)
                message = program.send(user_input)
            elif message.type  == MessageType.PRINT_OUTPUT:
                print_output(message.arg)
                message = next(program)
            elif message.type == MessageType.TERMINATE:
                final_output = message.arg
                should_continue = False
                break
    except StopIteration:
        pass
    return final_output

@pytest.mark.parametrize(
    "source_code,expected",
    [
        # Tests from day 2:
        ('1,9,10,3,2,3,11,0,99,30,40,50', [
         3500, 9, 10, 70, 2, 3, 11, 0, 99, 30, 40, 50]),
        ('1,0,0,0,99', [2, 0, 0, 0, 99]),
        ('2,3,0,3,99', [2, 3, 0, 6, 99]),
        ('2,4,4,5,99,0', [
            2, 4, 4, 5, 99, 9801]),
        ('1,1,1,4,99,5,6,0,99', [
            30, 1, 1, 4, 2, 5, 6, 0, 99]),
        # Tests from day 5 part 1:
        ('1002,4,3,4,33', [1002, 4, 3, 4, 99]),
        ('1101,100,-1,4,0', [1101, 100, -1, 4, 99]),
    ]
)
def test_simple_program(source_code, expected):
    assert run_with_input_output(source_code, input, print) == expected


equal_op_code_position_mode_program = '3,9,8,9,10,9,4,9,99,-1,8'
less_than_op_code_position_mode_program = '3,9,7,9,10,9,4,9,99,-1,8'
equal_op_code_immediate_mode_program = '3,3,1108,-1,8,3,4,3,99'
less_than_op_code_immediate_mode_program = '3,3,1107,-1,8,3,4,3,99'
jump_op_code_position_mode_program = '3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9'
jump_op_code_immediate_mode_program = '3,3,1105,-1,9,1101,0,0,12,4,12,99,1'
large_program = '3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99'


@pytest.mark.parametrize(
    "user_input_value,source_code,expected_output",
    [
        ("8", equal_op_code_position_mode_program, 1),
        ("13", equal_op_code_position_mode_program, 0),
        ("5", less_than_op_code_position_mode_program, 1),
        ("13", less_than_op_code_position_mode_program, 0),
        ("8", equal_op_code_immediate_mode_program, 1),
        ("13", equal_op_code_immediate_mode_program, 0),
        ("5", less_than_op_code_immediate_mode_program, 1),
        ("13", less_than_op_code_immediate_mode_program, 0),
        ("0", jump_op_code_position_mode_program, 0),
        ("100", jump_op_code_position_mode_program, 1),
        ("0", jump_op_code_immediate_mode_program, 0),
        ("100", jump_op_code_immediate_mode_program, 1),
        ("7", large_program, 999),
        ("8", large_program, 1000),
        ("9", large_program, 1001),
    ]
)
def test_programs_with_input_output(user_input_value, source_code, expected_output):
    get_user_input = Mock(return_value=user_input_value)
    print_output = Mock()
    run_with_input_output(source_code, get_user_input, print_output)
    print_output.assert_called_once_with(expected_output)

def execute_day_05_input(get_user_input=input, print_output=print):
    with open('day_05_input.txt') as f:
        source_code = f.readline()
        run_with_input_output(source_code, get_user_input, print_output)


def test_part_one():
    get_user_input = Mock(return_value="1")
    print_output = Mock()
    execute_day_05_input(get_user_input, print_output)
    assert print_output.call_args_list == [
        call(0),
        call(0),
        call(0),
        call(0),
        call(0),
        call(0),
        call(0),
        call(0),
        call(0),
        call(4601506),
    ]


def test_part_two():
    get_user_input = Mock(return_value="5")
    print_output = Mock()
    execute_day_05_input(get_user_input, print_output)
    print_output.assert_called_once_with(5525561)


if __name__ == "__main__":
    pass
