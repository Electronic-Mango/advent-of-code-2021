from collections import namedtuple
from heapq import heappush, heappop
from itertools import product
from numpy import full, array, ndindex, zeros
from sys import argv, maxsize

DEFAULT_INPUT_FILE_NAME = "input"
EXPAND_SIZE = 5
Position = namedtuple("Position", ["distance", "x", "y"])


def load_cave_risk_levels():
    with open(get_input_file_name()) as input_file:
        risk = [line.strip() for line in input_file.readlines()]
    risk = [list(line) for line in risk]
    risk = [map(int, line) for line in risk]
    risk = [list(line) for line in risk]
    return array(risk)


def get_input_file_name():
    return argv[1] if len(argv) == 2 else DEFAULT_INPUT_FILE_NAME


def task(position_risks):
    print(f"Running task for shape {position_risks.shape}...")
    total_risks = full(position_risks.shape, maxsize)
    total_risks[0][0] = 0
    positions_to_check = [Position(0, 0, 0)]
    while len(positions_to_check) != 0:
        populate_risks(positions_to_check, total_risks, position_risks)
    shortest_path = total_risks[-1][-1]
    print(f"Shortest path: {shortest_path}")
    print()


def populate_risks(positions_to_check, total_risks, position_risks):
    origin_position = heappop(positions_to_check)
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        adjacent_indexes = origin_position.x + dx, origin_position.y + dy
        if (not_valid_indexes(*adjacent_indexes, *position_risks.shape) or
            not_lower_risk(total_risks, origin_position, adjacent_indexes, position_risks)):
            continue
        if total_risks[adjacent_indexes] != maxsize:
            positions_to_check.remove(Position(total_risks[adjacent_indexes], *adjacent_indexes))
        origin_risk = total_risks[origin_position.x][origin_position.y]
        total_risks[adjacent_indexes] = origin_risk + position_risks[adjacent_indexes]
        heappush(positions_to_check, Position(total_risks[adjacent_indexes], *adjacent_indexes))


def not_valid_indexes(x, y, size_x, size_y):
    return not (0 <= x < size_x and 0 <= y < size_y)


def not_lower_risk(total_risks, origin_position, adjacent_indexes, risks):
    new_risk = total_risks[origin_position.x][origin_position.y] + risks[adjacent_indexes]
    existing_risk = total_risks[adjacent_indexes]
    return existing_risk <= new_risk


def expand_risks(initial_risks):
    initial_shape = initial_risks.shape
    new_shape = tuple(size * EXPAND_SIZE for size in initial_shape)
    expanded_risks = zeros(new_shape, dtype=int)
    for offsets in product(range(EXPAND_SIZE), range(EXPAND_SIZE)):
        increase_by = sum(offsets)
        start_index_offsets = tuple(size * offset for size, offset in zip(initial_shape, offsets))
        fill_array(initial_risks, expanded_risks, *start_index_offsets, increase_by)
    return expanded_risks


def fill_array(source, destination, offset_x, offset_y, increase_by):
    for x, y in ndindex(source.shape):
        new_indexes = offset_x + x, offset_y + y
        destination[new_indexes] = get_new_risk(source[x][y], increase_by)


def get_new_risk(initial_risk, increase_by):
    new_risk = (initial_risk + increase_by) % 9
    return new_risk if new_risk != 0 else 9


risk = load_cave_risk_levels()
task(risk)
new_risk = expand_risks(risk)
task(new_risk)
