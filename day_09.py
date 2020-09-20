from day_05 import run_with_input_output
from unittest.mock import Mock, call


def test_program_with_relative_base_1():
    print_output = Mock()
    run_with_input_output(
        "109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99", input, print_output
    )
    assert print_output.call_args_list == [
        call(109),
        call(1),
        call(204),
        call(-1),
        call(1001),
        call(100),
        call(1),
        call(100),
        call(1008),
        call(100),
        call(16),
        call(101),
        call(1006),
        call(101),
        call(0),
        call(99),
    ]


def test_program_with_relative_base_2():
    print_output = Mock()
    run_with_input_output("1102,34915192,34915192,7,4,7,99,0", input, print_output)
    print_output.assert_called_once_with(1219070632396864)


def test_program_with_relative_base_3():
    print_output = Mock()
    run_with_input_output("104,1125899906842624,99", input, print_output)
    print_output.assert_called_once_with(1125899906842624)


def execute_input_program(get_user_input=input, print_output=print):
    with open("day_09_input.txt") as f:
        source_code = f.readline()
        run_with_input_output(source_code, get_user_input, print_output)


# Note: These tests are commented out because the input and expected output are
# different for each Advent of Code participant. The tests as written below
# pass given my input and the correct output (as judged by the AoC website).
# def test_part_one():
#     print_output = Mock()
#     get_user_input = Mock(return_value="1")
#     execute_input_program(get_user_input, print_output)
#     print_output.assert_called_once_with(3839402290)
# def test_part_two():
#     print_output = Mock()
#     get_user_input = Mock(return_value="2")
#     execute_input_program(get_user_input, print_output)
#     print_output.assert_called_once_with(35734)


if __name__ == "__main__":
    execute_input_program()
