from collections import namedtuple
from itertools import chain, product
from math import floor, ceil
from sys import argv

DEFAULT_INPUT_FILE_NAME = "input"
INCREASE_DEPTH_CHARACTER = "["
DECREASE_DEPTH_CHARACTER = "]"
DEPTH_CHARACTERS = INCREASE_DEPTH_CHARACTER, DECREASE_DEPTH_CHARACTER
EXPAND_LIMIT = 4
SPLIT_LIMIT = 9
Node = namedtuple("Node", ["depth", "value"])


def load_snailnumbers():
    with open(get_input_file_name()) as input_file:
        return [parse_snailnumber(line.strip()) for line in input_file.readlines()]


def get_input_file_name():
    return argv[1] if len(argv) == 2 else DEFAULT_INPUT_FILE_NAME


def parse_snailnumber(line):
    snailnumber = []
    depth = 0
    for character in line:
        if character in DEPTH_CHARACTERS:
            depth += 1 if character == INCREASE_DEPTH_CHARACTER else -1
        elif character.isnumeric():
            snailnumber.append(Node(depth, int(character)))
    return snailnumber


def part1(all_snailnumbers):
    print(f"Running task 1...")
    magnitude = reduce_and_calculate_magnitude(all_snailnumbers)
    print(f"Total magnitude: {magnitude}")
    print()


def reduce_and_calculate_magnitude(all_snailnumbers):
    while len(all_snailnumbers) > 1:
        snailnumber = sum(all_snailnumbers[0], all_snailnumbers[1])
        all_snailnumbers = [reduce(snailnumber)] + all_snailnumbers[2:]
    return calculate_magnitude(*all_snailnumbers)


def sum(*snailnumber):
    return [Node(depth + 1, value) for depth, value in chain(*snailnumber)]


def reduce(snailnumber):
    while can_explode(snailnumber) or can_split(snailnumber):
        if can_explode(snailnumber):
            snailnumber = explode(snailnumber)
        else:
            snailnumber = split(snailnumber)
    return snailnumber


def can_explode(snailnumber):
    return any(depth > EXPAND_LIMIT for depth, _ in snailnumber)


def can_split(snailnumber):
    return any(value > SPLIT_LIMIT for _, value in snailnumber)


def explode(snailnumber):
    for i in range(len(snailnumber) - 1):
        node_1, node_2 = snailnumber[i], snailnumber[i + 1]
        if node_1.depth > EXPAND_LIMIT and node_2.depth > EXPAND_LIMIT:
            break
    previous_snailnumbers = previous_snailnumbers_after_explode(snailnumber, i, node_1)
    next_snailnumbers = next_snailnumbers_after_explode(snailnumber, i + 1, node_2)
    return previous_snailnumbers + [Node(node_1.depth - 1, 0)] + next_snailnumbers


def previous_snailnumbers_after_explode(snailnumber, exploding_index, node_1):
    if exploding_index <= 0:
        return []
    previous_node = snailnumber[exploding_index - 1]
    new_previous_node = Node(previous_node.depth, previous_node.value + node_1.value)
    return snailnumber[: exploding_index - 1] + [new_previous_node]


def next_snailnumbers_after_explode(snailnumber, exploding_index, node_2):
    if exploding_index >= len(snailnumber) - 1:
        return []
    next_node = snailnumber[exploding_index + 1]
    new_next_node = Node(next_node.depth, next_node.value + node_2.value)
    return [new_next_node] + snailnumber[exploding_index + 2 :]


def split(snailnumber):
    split_index, node = get_split_node_and_index(snailnumber)
    return [
        *snailnumber[: max(split_index, 0)],
        Node(node.depth + 1, floor(node.value / 2)),
        Node(node.depth + 1, ceil(node.value / 2)),
        *snailnumber[split_index + 1 :]
    ]


def get_split_node_and_index(snailnumber):
    return next((index, node) for index, node in enumerate(snailnumber) if node.value > SPLIT_LIMIT)


def calculate_magnitude(snailnumber):
    while len(snailnumber) > 1:
        max_depth_index = get_max_depth_index(snailnumber)
        node_1, node_2 = snailnumber[max_depth_index], snailnumber[max_depth_index + 1]
        snailnumber = [
            *snailnumber[: max(max_depth_index, 0)],
            Node(node_1.depth - 1, 3 * node_1.value + 2 * node_2.value),
            *snailnumber[max_depth_index + 2 :]
        ]
    return snailnumber[0].value


def get_max_depth_index(snailnumber):
    max_depth = max(depth for depth, _ in snailnumber)
    return next(index for index, node in enumerate(snailnumber) if node.depth == max_depth)


def part2(snailnumbers):
    print(f"Running task 2...")
    magnitudes = [
        reduce_and_calculate_magnitude([snailnumbers[first], snailnumbers[second]])
        for first, second in product(range(len(snailnumbers)), range(len(snailnumbers)))
        if first != second
    ]
    print(f"Highest possible magnitude: {max(magnitudes)}")
    print()


snailnumbers = load_snailnumbers()
part1(snailnumbers)
part2(snailnumbers)
