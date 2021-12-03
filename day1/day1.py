from sys import argv

DEFAULT_INPUT_FILE_NAME = "input"


def get_input_file_name():
    return argv[1] if len(argv) == 2 else DEFAULT_INPUT_FILE_NAME


def load_measurements():
    input_file_name = get_input_file_name()
    with open(input_file_name) as input_file:
        return [int(measurement.strip()) for measurement in input_file.readlines()]


def get_number_of_increments(measurements):
    return len([0 for previous, next in zip(measurements, measurements[1:]) if next > previous])


def part1(measurements):
    print("Running part 1...")
    number_of_increments = get_number_of_increments(measurements)
    print("Result is: {}".format(number_of_increments))
    print()


def concatenate_measurements_in_triplets(measurements):
    return [sum(triplet) for triplet in zip(measurements, measurements[1:], measurements[2:])]


def part2(measurements):
    print("Running part 2...")
    concatenated_measurements = concatenate_measurements_in_triplets(measurements)
    number_of_increments = get_number_of_increments(concatenated_measurements)
    print("Result is: {}".format(number_of_increments))
    print()


measurements = load_measurements()
part1(measurements)
part2(measurements)
