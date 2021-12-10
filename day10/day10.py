from collections import deque
from functools import reduce
from statistics import median
from sys import argv

DEFAULT_INPUT_FILE_NAME = "input"
OPEN_TO_CLOSE_BRACKET = {
    "(": ")",
    "[": "]",
    "{": "}",
    "<": ">"
}
INCORRECT_BRACKET_VALUE = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137
}
MISSING_BRACKET_VALUE = {
    "(": 1,
    "[": 2,
    "{": 3,
    "<": 4
}
CORRUPTED = True
NOT_CORRUPTED = False


def load_navigation_data():
    with open(get_input_file_name()) as input_file:
        return [chunks.strip() for chunks in input_file.readlines()]


def get_input_file_name():
    return argv[1] if len(argv) == 2 else DEFAULT_INPUT_FILE_NAME


def task(navigation_data):
    print("Running part 1 and 2...")
    error_values = [get_line_error_value(line) for line in navigation_data]
    corrupted = [error for corrupted, error in error_values if corrupted]
    incomplete = [error for corrupted, error in error_values if not corrupted]
    total_corrupted_error = sum(corrupted)
    middle_incomplete_error = median(incomplete)
    print(f"Total corrupted error: {total_corrupted_error}")
    print(f"Middle incomplete error: {middle_incomplete_error}")


def get_line_error_value(line):
    opening_brackets = deque()
    for bracket in list(line):
        if bracket in OPEN_TO_CLOSE_BRACKET.keys():
            opening_brackets.append(bracket)
        else:
            last_opening_character = opening_brackets.pop()
            expected_closing_character = OPEN_TO_CLOSE_BRACKET[last_opening_character]
            if expected_closing_character != bracket:
                return CORRUPTED, INCORRECT_BRACKET_VALUE[bracket]
    return NOT_CORRUPTED, get_missing_brackets_error_value(reversed(opening_brackets))


def get_missing_brackets_error_value(brackets):
    return reduce(lambda score, bracket: score * 5 + MISSING_BRACKET_VALUE[bracket], brackets, 0)


navigation_data = load_navigation_data()
task(navigation_data)
