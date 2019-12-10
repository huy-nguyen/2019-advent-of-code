from typing import List
from day_05 import compile_source_code, run_with_input_output, MessageType
import pytest
import itertools
from collections import namedtuple


def get_user_input(return_values: List[int]):
    """Simulate user input by returning stringified versions of a predetermined list of integers"""
    index = 0

    def user_input(_):
        nonlocal index
        to_be_returned = str(return_values[index])
        index += 1
        return to_be_returned
    return user_input


def test_get_user_input():
    func = get_user_input([1, 2, 3])
    assert func('') == "1"
    assert func('') == "2"
    assert func('') == "3"
    with pytest.raises(Exception):
        assert func('')


class Custom_Output:
    """Simulate stdout by recording the values that the program prints to stdout"""

    def __init__(self):
        self.call_args: List[int] = []

    def __call__(self, arg: int):
        self.call_args.append(arg)

    def get_call_args(self):
        return self.call_args


def test_custom_output():
    output = Custom_Output()
    output(1)
    output(2)
    assert output.get_call_args() == [1, 2]


def run_amplifiers_once(source_code: str, phases: List[int]):
    prev_stage_output = 0
    for phase in phases:
        user_input = get_user_input([phase, prev_stage_output])
        print_output = Custom_Output()
        run_with_input_output(source_code, user_input, print_output)
        call_args = print_output.get_call_args()
        prev_stage_output = call_args[0]
    return prev_stage_output


def test_run_amplifiers():
    assert run_amplifiers_once("3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0", [
        4, 3, 2, 1, 0]) == 43210
    assert run_amplifiers_once(
        "3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0", [0, 1, 2, 3, 4]) == 54321
    assert run_amplifiers_once(
        "3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0", [1, 0, 4, 3, 2]) == 65210


def find_max_phase_settings_part_one(program: str) -> int:
    max_thruster_signal: int = - float("inf")
    for tup in itertools.permutations(range(0, 5), 5):
        phases = list(tup)
        thruster_signal = run_amplifiers_once(program, phases)
        if thruster_signal > max_thruster_signal:
            max_thruster_signal = thruster_signal
    return max_thruster_signal


def test_find_max_phase_settings_part_one():
    assert find_max_phase_settings_part_one(
        "3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0") == 43210
    assert find_max_phase_settings_part_one(
        "3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0") == 54321
    assert find_max_phase_settings_part_one(
        "3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0") == 65210


def part_one():
    with open('day_07_input.txt') as f:
        raw_input = f.readline()
        return find_max_phase_settings_part_one(raw_input)


Amplifier = namedtuple(
    "ProgramGroup", ["name", "program", "phase", "last_message"])


def run_amplifiers_continuously(source_code: str, phases: List[int]):
    amplifiers = [
        Amplifier(name=name, program=compile_source_code(
            source_code), phase=phase, last_message=None)
        for (name, phase) in zip(["A", "B", "C", "D", "E"], phases)
    ]

    current_amplifier_index = 0
    input_call_count = 0
    prev_amp_output = 0
    last_amplifier_name = None
    is_first_pass = True
    while True:
        current_amplifier = amplifiers[current_amplifier_index]
        if current_amplifier.name != last_amplifier_name:
            if current_amplifier.name == "A" and last_amplifier_name == "E":
                is_first_pass = False
            if current_amplifier.last_message is None:
                message = next(current_amplifier.program)
            elif last_amplifier_name == None:
                message = next(current_amplifier.program)
            else:
                message = current_amplifier.last_message
        else:
            message = current_amplifier.last_message
        last_amplifier_name = current_amplifier.name
        if message.type == MessageType.GET_INPUT:
            # On the first pass, we'll have to provide the phase setting then the output from the previous amplifier
            # but on subsequent passes, we'll only pass in the output from the previous amplifier.
            if is_first_pass:
                if input_call_count == 0:
                    input_call_count += 1
                    message = current_amplifier.program.send(
                        current_amplifier.phase)
                elif input_call_count == 1:
                    input_call_count += 1
                    message = current_amplifier.program.send(prev_amp_output)
                else:
                    raise RuntimeError(
                        "Each amplifier should not ask for more than 2 inputs in one run")
            else:
                message = current_amplifier.program.send(prev_amp_output)
            modified_current_amplifier = Amplifier(
                name=current_amplifier.name,
                program=current_amplifier.program,
                phase=current_amplifier.phase,
                last_message=message
            )
            amplifiers[current_amplifier_index] = modified_current_amplifier
        elif message.type == MessageType.PRINT_OUTPUT:
            prev_amp_output = message.arg
            modified_current_amplifier = Amplifier(
                name=current_amplifier.name,
                program=current_amplifier.program,
                phase=current_amplifier.phase,
                last_message=None
            )
            amplifiers[current_amplifier_index] = modified_current_amplifier
            # Advance to next amplifier:
            current_amplifier_index = 0 if current_amplifier_index == len(
                amplifiers) - 1 else current_amplifier_index + 1
            input_call_count = 0
        elif message.type == MessageType.TERMINATE:
            index_to_delete = current_amplifier_index
            current_amplifer_name = current_amplifier.name
            # Remove current amplifier from list of available amplifiers:
            del amplifiers[index_to_delete]
            input_call_count = 0
            # Program is done executing When amplifier E terminates:
            if current_amplifer_name == "E":
                return prev_amp_output


@pytest.mark.parametrize(
    "source_code,phases,expected",
    [
        ("3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5",
         [9, 8, 7, 6, 5], 139629729),
        ("3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10",
         [9, 7, 8, 5, 6], 18216)
    ]
)
def test_run_amplifiers_continuously(source_code, phases, expected):
    assert run_amplifiers_continuously(source_code, phases) == expected


def test_part_one():
    assert part_one() == 21000


def find_max_phase_settings_part_two(program: str) -> int:
    max_thruster_signal: float = - float("inf")
    for tup in itertools.permutations(range(5, 10), 5):
        phases = list(tup)
        thruster_signal = run_amplifiers_continuously(program, phases)
        if thruster_signal > max_thruster_signal:
            max_thruster_signal = thruster_signal
    return int(max_thruster_signal)


def test_find_max_phase_settings_part_two():
    assert find_max_phase_settings_part_two(
        "3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5") == 139629729
    assert find_max_phase_settings_part_two(
        "3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10") == 18216


def part_two():
    with open('day_07_input.txt') as f:
        raw_input = f.readline()
        return find_max_phase_settings_part_two(raw_input)


def test_part_two():
    assert part_two() == 61379886


if __name__ == "__main__":
    pass
