from sys import argv

DEFAULT_INPUT_FILE_NAME = "input"


def load_input():
    with open(get_input_file_name()) as input_file:
        return [line.strip() for line in input_file.readlines()]


def get_input_file_name():
    return argv[1] if len(argv) == 2 else DEFAULT_INPUT_FILE_NAME


def part1(input):
    print("Running part 1...")

    print(f"Result:")
    print()


def part2(input):
    print("Running part 2...")

    print(f"Result:")
    print()


input = load_input()
part1(input)
part2(input)
