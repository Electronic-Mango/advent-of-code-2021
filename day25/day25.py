from numpy import array, array_equal, ndindex, zeros
from sys import argv

DEFAULT_INPUT_FILE_NAME = "input"
EMPTY = "."
RIGHT = ">"
DOWN = "v"


def load_cucumbers():
    with open(get_input_file_name()) as input_file:
        cucumbers = [line.strip() for line in input_file.readlines()]
    cucumbers = [list(line) for line in cucumbers]
    return array(cucumbers, dtype=str)


def get_input_file_name():
    return argv[1] if len(argv) == 2 else DEFAULT_INPUT_FILE_NAME


def task(cucumbers):
    print("Running part 1...")
    cucumbers_before = zeros(cucumbers.shape)
    steps = 0
    while not array_equal(cucumbers, cucumbers_before):
        cucumbers_before = cucumbers.copy()
        cucumbers = move_cucumbers(cucumbers, RIGHT, next_right_index)
        cucumbers = move_cucumbers(cucumbers, DOWN, next_down_index)
        steps += 1
    print(f"Cucumbers stop moving after {steps} steps.")
    print()


def move_cucumbers(cucumbers, direction, next_index_function):
    cucumbers_after = cucumbers.copy()
    for index in ndindex(cucumbers.shape):
        if cucumbers[index] != direction:
            continue
        next_index = next_index_function(*index, *cucumbers.shape)
        if cucumbers[next_index] != EMPTY:
            continue
        cucumbers_after[index] = EMPTY
        cucumbers_after[next_index] = direction
    return cucumbers_after


def next_right_index(x, y, _, shape_y):
    return x, next_index(y, shape_y)


def next_down_index(x, y, shape_x, _):
    return next_index(x, shape_x), y


def next_index(index, limit):
    return index + 1 if index + 1 < limit else 0


cucumbers = load_cucumbers()
task(cucumbers)
