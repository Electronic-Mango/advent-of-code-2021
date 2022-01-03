from collections import namedtuple
from sys import argv

DEFAULT_INPUT_FILE_NAME = "input"
SINGLE_INPUT_PROGRAM_SIZE = 18
INPUT_DIGIT_SIZE = 14
SHOULD_PUSH_TO_STACK_INDEX = 4
SHOULD_PUSH_TO_STACK_VALUE = "1"
PUSH_TO_STACK_VALUE_INDEX = 15
POP_FROM_STACK_VALUE_INDEX = 5

Instruction = namedtuple("Instruction", ["push_to_stack", "push_value", "pop_value"])


def load_monad():
    with open(get_input_file_name()) as input_file:
        monad = [line.strip() for line in input_file.readlines()]
    monad = [instruction.split()[-1] for instruction in monad]
    monad = [
        monad[instruction : instruction + SINGLE_INPUT_PROGRAM_SIZE]
        for instruction in range(0, len(monad), SINGLE_INPUT_PROGRAM_SIZE)
    ]
    monad = [parse_instructions(instructions) for instructions in monad]
    return monad


def get_input_file_name():
    return argv[1] if len(argv) == 2 else DEFAULT_INPUT_FILE_NAME


def parse_instructions(instructions):
    push_to_stack = instructions[SHOULD_PUSH_TO_STACK_INDEX] == SHOULD_PUSH_TO_STACK_VALUE
    push_value = int(instructions[PUSH_TO_STACK_VALUE_INDEX])
    pop_value = int(instructions[POP_FROM_STACK_VALUE_INDEX])
    return Instruction(push_to_stack, push_value, pop_value)


def task(monad):
    print("Running part 1 & 2...")
    relations = calculate_relations(monad)
    max_model_number = calculate_max_model_number(relations)
    min_model_number = calculate_min_model_number(relations)
    print(f"Largest accepted model number:  {max_model_number}")
    print(f"Smallest accepted model number: {min_model_number}")
    print()


def calculate_relations(monad):
    instruction_stack, relations = list(), list()
    for index, instruction in enumerate(monad):
        if instruction.push_to_stack:
            instruction_stack += [(range(INPUT_DIGIT_SIZE)[index], instruction.push_value)]
        else:
            relations += [prepare_relation(index, instruction.pop_value, *instruction_stack.pop())]
    return relations


def prepare_relation(index, pop_value, first_digit, value):
    second_digit = range(INPUT_DIGIT_SIZE)[index]
    value += pop_value
    return first_digit, second_digit, value


def calculate_max_model_number(relations):
    digit = [9] * INPUT_DIGIT_SIZE
    for first_digit, second_digit, value in relations:
        digit_to_modify = first_digit if value > 0 else second_digit
        digit[digit_to_modify] -= abs(value)
    return int("".join(map(str, digit)))


def calculate_min_model_number(relations):
    digit = [1] * INPUT_DIGIT_SIZE
    for first_digit, second_digit, value in relations:
        digit_to_modify = second_digit if value > 0 else first_digit
        digit[digit_to_modify] += abs(value)
    return int("".join(map(str, digit)))


monad = load_monad()
task(monad)
