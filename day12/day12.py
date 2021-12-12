from collections import defaultdict
from sys import argv

DEFAULT_INPUT_FILE_NAME = "input"
START_CAVE = "start"
END_CAVE = "end"


def load_cave_connections():
    with open(get_input_file_name()) as input_file:
        cave_pairs = [line.strip().split("-") for line in input_file.readlines()]
    cave_connections = defaultdict(list)
    for cave1, cave2 in cave_pairs:
        cave_connections[cave1].append(cave2)
        cave_connections[cave2].append(cave1)
    return cave_connections


def get_input_file_name():
    return argv[1] if len(argv) == 2 else DEFAULT_INPUT_FILE_NAME


def task(cave_connections, part_number):
    print(f"Running part {part_number}...")
    all_paths = set()
    find_paths(all_paths, START_CAVE, [START_CAVE], cave_connections, part_number)
    number_of_paths = len(all_paths)
    print(f"Total number of paths: {number_of_paths}")
    print()


def find_paths(all_paths, current_cave, path, cave_connections, part_number):
    for next_cave in cave_connections[current_cave]:
        if next_cave == END_CAVE:
            all_paths.add(tuple(path))
        elif can_visit_cave(next_cave, path, part_number):
            find_paths(all_paths, next_cave, path + [next_cave], cave_connections, part_number)


def can_visit_cave(cave, path, part_number):
    # Cave is either large or small, but not visited yet.
    can_visit = cave.isupper() or cave not in path
    # Cave is small and already visited, but for part 2 one small cave can be visited twice.
    # Otherwise there is no impact on whether cave can be visited or not.
    can_visit |= part_number == 2 and all(path.count(cave) <= 1 for cave in path if cave.islower())
    # Cave is not the starting one.
    can_visit &= cave != START_CAVE
    return can_visit


cave_connections = load_cave_connections()
task(cave_connections, part_number=1)
task(cave_connections, part_number=2)
