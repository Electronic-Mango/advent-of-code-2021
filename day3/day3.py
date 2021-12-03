from bitstring import BitArray
from numpy import array, delete, mean, where
from statistics import mode
from sys import argv

DEFAULT_INPUT_FILE_NAME = "input"


def get_input_file_name():
    return argv[1] if len(argv) == 2 else DEFAULT_INPUT_FILE_NAME


def load_measurements():
    input_file_name = get_input_file_name()
    with open(input_file_name) as input_file:
        return [[int(bit) for bit in measurement.strip()] for measurement in input_file.readlines()]


def bit_array_to_int(bit_array):
    return BitArray(bit_array).uint


def part1(transposed_measurements):
    print("Running part 1...")
    gamma_bit_array = [mode(bits) for bits in transposed_measurements]
    epsilon_bit_array = [bit ^ 0b1 for bit in gamma_bit_array]
    gamma = bit_array_to_int(gamma_bit_array)
    epsilon = bit_array_to_int(epsilon_bit_array)
    power_consumption = gamma * epsilon
    print("Gamma rate: {}".format(gamma))
    print("Epsilon rate: {}".format(epsilon))
    print("Power consumption: {}".format(power_consumption))
    print()


def get_rating(rating_candidates, bit_to_delete_from_column_mean):
    bit_column = 0
    while rating_candidates.shape[1] > 1:
        mean_value_of_column = mean(rating_candidates[bit_column])
        bit_to_delete = bit_to_delete_from_column_mean(mean_value_of_column)
        rating_candidates = delete(
            rating_candidates,
            where(rating_candidates[bit_column] == bit_to_delete),
            axis=1,
        )
        bit_column += 1
    return bit_array_to_int(rating_candidates.flatten())


def part2(transposed_measurements):
    print("Running part 2...")
    # I used those lambdas due to Python rounding halfs to even numbers rather than up.
    oxygen_rating = get_rating(transposed_measurements, lambda mean: 0 if mean >= 0.5 else 1)
    scrubber_rating = get_rating(transposed_measurements, lambda mean: 1 if mean >= 0.5 else 0)
    life_support_rating = oxygen_rating * scrubber_rating
    print("Oxygen generator rating: {}".format(oxygen_rating))
    print("CO2 scrubber rating: {}".format(scrubber_rating))
    print("Life support rating: {}".format(life_support_rating))
    print()


measurements = load_measurements()
transposed_measurements = array(measurements).T
part1(transposed_measurements)
part2(transposed_measurements)
