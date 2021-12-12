from itertools import product
from numpy import array, ndindex
from sys import argv

DEFAULT_INPUT_FILE_NAME = "input"
PART_1_STEPS = 100
FLASHING_POINT = 10
LOW_ENERGY_LEVEL = 0


def load_octopuses():
    with open(get_input_file_name()) as input_file:
        octopuses = [line.strip() for line in input_file.readlines()]
    octopuses = [map(int, line) for line in octopuses]
    octopuses = [list(line) for line in octopuses]
    return array(octopuses)


def get_input_file_name():
    return argv[1] if len(argv) == 2 else DEFAULT_INPUT_FILE_NAME


def part1(octopuses):
    print("Running part 1...")
    number_of_flashes = sum([get_number_of_flashes(octopuses) for _ in range(PART_1_STEPS)])
    print(f"Total number of flashes: {number_of_flashes}")
    print()


def get_number_of_flashes(octopuses):
    octopuses += 1
    flashes = set()
    for octopus in ndindex(octopuses.shape):
        flash(*octopus, octopuses, flashes)
    octopuses[octopuses >= FLASHING_POINT] = LOW_ENERGY_LEVEL
    return len(flashes)


def flash(x, y, octopuses, flashes):
    if octopuses[x][y] < FLASHING_POINT or (x, y) in flashes:
        return
    flashes.add((x, y))
    for dx, dy in product([-1, 0, 1], repeat=2):
        adjacent_x, adjacent_y = x + dx, y + dy
        size_x, size_y = octopuses.shape
        if 0 <= adjacent_x < size_x and 0 <= adjacent_y < size_y:
            octopuses[adjacent_x][adjacent_y] += 1
            flash(adjacent_x, adjacent_y, octopuses, flashes)


def part2(octopuses):
    print("Running part 2...")
    step = 1
    while get_number_of_flashes(octopuses) != octopuses.size:
        step += 1
    print(f"All flash at step: {step}")
    print()


octopuses = load_octopuses()
part1(octopuses.copy())
part2(octopuses.copy())
