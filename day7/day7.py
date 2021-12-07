from math import ceil, floor
from statistics import mean, median
from sys import argv

DEFAULT_INPUT_FILE_NAME = "input"


def load_crabs():
    with open(get_input_file_name()) as input_file:
        return [int(position) for position in input_file.readline().strip().split(",")]


def get_input_file_name():
    return argv[1] if len(argv) == 2 else DEFAULT_INPUT_FILE_NAME


def task_brute_force(crabs, fuel_consumption_function, part_number):
    print(f"Running part {part_number}...")
    fuel_costs_for_each_target = [
        sum([fuel_consumption_function(current, target) for current in crabs])
        for target in range(min(crabs), max(crabs))
    ]
    print(f"Lowest fuel consumption: {min(fuel_costs_for_each_target)}")


def fuel_consumption(crabs, target, target_rounding_function, fuel_consumption_function):
    target = target_rounding_function(target)
    fuel_changes = [fuel_consumption_function(value, target) for value in crabs]
    return sum(fuel_changes)


def task_smart(crabs, target_function, fuel_consumption_function, part_number):
    print(f"Running part {part_number}...")
    target = target_function(crabs)
    target_lower, target_upper = floor(target), ceil(target)
    fuel_changes_lower = [fuel_consumption_function(value, target_upper) for value in crabs]
    fuel_changes_upper = [fuel_consumption_function(value, target_lower) for value in crabs]
    total_fuel_consumption = min(sum(fuel_changes_lower), sum(fuel_changes_upper))
    print(f"Lowest fuel consumption: {total_fuel_consumption}")


def linear_fuel_consumption(current, target):
    return abs(current - target)


def arythmetic_fuel_consumption(current, target):
    distance_to_target = abs(current - target)
    return ((distance_to_target ** 2) + distance_to_target) / 2


crab_positions = load_crabs()

task_brute_force(crab_positions, linear_fuel_consumption, part_number=1)
task_brute_force(crab_positions, arythmetic_fuel_consumption, part_number=2)

task_smart(crab_positions, median, linear_fuel_consumption, part_number=1)
task_smart(crab_positions, mean, arythmetic_fuel_consumption, part_number=2)
