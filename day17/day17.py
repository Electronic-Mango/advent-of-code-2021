from collections import namedtuple
from itertools import product
from re import findall
from sys import argv

DEFAULT_INPUT_FILE_NAME = "input"
Target = namedtuple("Target", ["x_min", "x_max", "y_min", "y_max"])


def load_target():
    with open(get_input_file_name()) as input_file:
        target = input_file.readline().strip()
    target = findall("-?[\d]+", target)
    target = map(int, target)
    return Target(*target)


def get_input_file_name():
    return argv[1] if len(argv) == 2 else DEFAULT_INPUT_FILE_NAME


def part1(target):
    print(f"Running task 1...")
    max_altitude = (abs(target.y_min) - 1) * abs(target.y_min) // 2
    print(f"Highest altitude: {max_altitude}")
    print()


def part2(target):
    print(f"Running task 2...")
    velocity_results = [run_probe(target, *velocity) for velocity in get_velocity_range(target)]
    hitting_altitudes = sum(near_target for near_target in velocity_results)
    print(f"Hitting velocities: {hitting_altitudes}")
    print()


def get_velocity_range(target):
    range_x = range(1, target.x_max + 1)
    range_y = range(target.y_min, -target.y_min)
    return product(range_x, range_y)


def run_probe(target, velocity_x, velocity_y):
    position_x, position_y = 0, 0
    near_target = False
    while position_x <= target.x_max and position_y >= target.y_min and not near_target:
        position_x = position_x + velocity_x
        position_y = position_y + velocity_y
        velocity_x = max(velocity_x - 1, 0)
        velocity_y = velocity_y - 1
        near_target = probe_near_target(target, position_x, position_y)
    return near_target


def probe_near_target(target, position_x, position_y):
    return target.x_min <= position_x <= target.x_max and target.y_min <= position_y <= target.y_max


target = load_target()
part1(target)
part2(target)
