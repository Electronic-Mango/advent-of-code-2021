from sys import argv

DEFAULT_INPUT_FILE_NAME = "input"
FORWARD_COMMAND = "forward"
DOWN_COMMAND = "down"
UP_COMMAND = "up"
DEPTH_COMMAND = "depth"


def get_input_file_name():
    return argv[1] if len(argv) == 2 else DEFAULT_INPUT_FILE_NAME


def load_commands():
    input_file_name = get_input_file_name()
    with open(input_file_name) as input_file:
        commands = [line.strip().split(" ") for line in input_file.readlines()]
    commands = [(command, int(value)) for command, value in commands]
    return [unify_depth_commands(command, value) for command, value in commands]


def unify_depth_commands(command, value):
    if command not in [DOWN_COMMAND, UP_COMMAND]:
        return command, value
    unified_value = value if command == DOWN_COMMAND else -value
    return DEPTH_COMMAND, unified_value


def print_position(horizontal_position, vertical_position):
    final_position = horizontal_position * vertical_position
    print("Horizontal position: {}".format(horizontal_position))
    print("Vertical position: {}".format(vertical_position))
    print("Final position: {}".format(final_position))


def part1(commands):
    print("Running part 1...")
    horizontal_position = 0
    vertical_position = 0
    for [command, value] in commands:
        if command == FORWARD_COMMAND:
            horizontal_position += value
        elif command == DEPTH_COMMAND:
            vertical_position += value
    print_position(horizontal_position, vertical_position)
    print()


def part2(commands):
    print("Running part 2...")
    horizontal_position = 0
    vertical_position = 0
    aim = 0
    for [command, value] in commands:
        if command == FORWARD_COMMAND:
            horizontal_position += value
            vertical_position += aim * value
        elif command == DEPTH_COMMAND:
            aim += value
    print_position(horizontal_position, vertical_position)
    print()


commands = load_commands()
part1(commands)
part2(commands)
