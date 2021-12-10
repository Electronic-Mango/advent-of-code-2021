from collections import Counter
from numpy import linspace
from sys import argv

DEFAULT_INPUT_FILE_NAME = "input"


def load_vent_lines():
    with open(get_input_file_name()) as input_file:
        input_lines = [line.strip() for line in input_file.readlines()]
    vent_lines = [line.split(" -> ") for line in input_lines]
    vent_lines = [(start.split(","), end.split(",")) for start, end in vent_lines]
    return [((int(x), int(y)) for x, y in line) for line in vent_lines]


def get_input_file_name():
    return argv[1] if len(argv) == 2 else DEFAULT_INPUT_FILE_NAME


def convert_edge_coordinates_to_lines(start, end):
    start_x, start_y = start
    end_x, end_y = end
    span_x = abs(end_x - start_x) + 1
    span_y = abs(end_y - start_y) + 1
    span = max(span_x, span_y)
    coordinates_x = linspace(start_x, end_x, span)
    coordinates_y = linspace(start_y, end_y, span)
    line = zip(coordinates_x, coordinates_y)
    return list(line)


def is_straight(vent_line):
    start_x, start_y = vent_line[0]
    end_x, end_y = vent_line[-1]
    return start_x == end_x or start_y == end_y


def task(vent_lines, part_number):
    print(f"Running part {part_number}...")
    all_points = [point for line in vent_lines for point in line]
    overlapping_points = [point for point, count in Counter(all_points).items() if count > 1]
    number_of_overlapping_points = len(overlapping_points)
    print(f"Overlapping vent lines: {number_of_overlapping_points}")
    print()


vent_edge_coordinates = load_vent_lines()
vent_lines = [convert_edge_coordinates_to_lines(start, end) for start, end in vent_edge_coordinates]
straight_vent_lines = [line for line in vent_lines if is_straight(line)]
task(straight_vent_lines, part_number=1)
task(vent_lines, part_number=2)
