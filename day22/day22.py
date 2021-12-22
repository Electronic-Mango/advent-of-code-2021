from collections import defaultdict, namedtuple
from math import prod
from re import findall
from sys import argv

DEFAULT_INPUT_FILE_NAME = "input"
STATE_ON = "on"
NUMBER_REGEX = r"-?\d+"
INITIALIZATION_RANGE_START = -50
INITIALIZATION_RANGE_END = 50

Range = namedtuple("Range", ["start", "end"])
Cube = namedtuple("Cube", ["x", "y", "z"])


def load_instructions():
    with open(get_input_file_name()) as input_file:
        instructions = [line.strip() for line in input_file.readlines()]
    instructions = [line.split() for line in instructions]
    instructions = [(state == STATE_ON, coordinates) for state, coordinates in instructions]
    instructions = [(state, parse_coordinates(coordinates)) for state, coordinates in instructions]
    return instructions


def get_input_file_name():
    return argv[1] if len(argv) == 2 else DEFAULT_INPUT_FILE_NAME


def parse_coordinates(coordinates):
    coordinates = coordinates.split(",")
    coordinates = (findall(NUMBER_REGEX, coordinate) for coordinate in coordinates)
    coordinates = (Range(*map(int, coordinate)) for coordinate in coordinates)
    return Cube(*coordinates)


def task(instructions):
    print("Running part 1 & 2...")
    all_cubes = defaultdict(int)
    for state, cube in instructions:
        all_cubes = handle_cube(state, cube, all_cubes)
    limited_cubes = limit_all_cubes(all_cubes, INITIALIZATION_RANGE_START, INITIALIZATION_RANGE_END)
    cubes_on_reboot = cubes_on(all_cubes)
    cubes_on_initialization = cubes_on(limited_cubes)
    print(f"Cubes on after initialization: {cubes_on_initialization}")
    print(f"Cubes on after reboot: {cubes_on_reboot}")
    print()


def handle_cube(state, new_cube, all_cubes):
    for existing_cube, occurences in all_cubes.copy().items():
        intersection = intersect(existing_cube, new_cube)
        if intersection:
            all_cubes[intersection] -= occurences
    if state:
        all_cubes[new_cube] += 1
    all_cubes = {cube: occurences for cube, occurences in all_cubes.items() if occurences}
    return defaultdict(int, all_cubes)


def intersect(cube_1, cube_2):
    ranges = tuple(intersecting_range(*ranges) for ranges in zip(cube_1, cube_2))
    if ranges_are_valid(ranges):
        return Cube(*ranges)


def ranges_are_valid(ranges):
    return all(start <= end for start, end in ranges)


def intersecting_range(range_1, range_2):
    return Range(max(range_1.start, range_2.start), min(range_1.end, range_2.end))


def limit_all_cubes(cubes, min_value, max_value):
    limited_cubes = {
        limit_cube(cube, min_value, max_value): occurences for cube, occurences in cubes.items()
    }
    return {cube: occurences for cube, occurences in limited_cubes.items() if cube}


def limit_cube(cube, min_value, max_value):
    ranges = tuple(Range(max(start, min_value), min(end, max_value)) for start, end in cube)
    if ranges_are_valid(ranges):
        return Cube(*ranges)


def cubes_on(cubes):
    return sum(cube_size(cube) * occurences for cube, occurences in cubes.items())


def cube_size(cube):
    return prod(end - start + 1 for start, end in cube)  # + 1 for cuboid at indexes 0


instructions = load_instructions()
task(instructions)
