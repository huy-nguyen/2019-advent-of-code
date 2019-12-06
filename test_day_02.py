from day_02 import execute_program, parse_input, part_one, part_two


def test_execute_program():
    assert execute_program(parse_input('1,9,10,3,2,3,11,0,99,30,40,50')) == [
        3500, 9, 10, 70, 2, 3, 11, 0, 99, 30, 40, 50]
    assert execute_program(parse_input('1,0,0,0,99')) == [2, 0, 0, 0, 99]
    assert execute_program(parse_input('2,3,0,3,99')) == [2, 3, 0, 6, 99]
    assert execute_program(parse_input('2,4,4,5,99,0')) == [
        2, 4, 4, 5, 99, 9801]
    assert execute_program(parse_input('1,1,1,4,99,5,6,0,99')) == [
        30, 1, 1, 4, 2, 5, 6, 0, 99]


def test_part_one():
    assert part_one()[0] == 4090689


def test_part_two():
    assert part_two() == 7733
