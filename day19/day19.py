from collections import Counter, deque
from itertools import permutations, product
from os import linesep
from sys import argv

DEFAULT_INPUT_FILE_NAME = "input"
EXPECTED_OVERLAPPING_BEACONS = 12
AXIS_PERMUTATION = list(permutations([0, 1, 2]))
ROTATION_PRODUCT = list(product([1, -1], repeat=3))
TRANSFORMATIONS = list(product(AXIS_PERMUTATION, ROTATION_PRODUCT))
# Still not great - there're twice as many transformations as needed.


def load_scanner_data():
    with open(get_input_file_name()) as input_file:
        scanners = input_file.read().strip()
    scanners = scanners.split(linesep + linesep)
    scanners = [scanner.splitlines()[1:] for scanner in scanners]
    scanners = [map(lambda beacon: beacon.split(","), beacons) for beacons in scanners]
    scanners = [map(lambda beacon: tuple(map(int, beacon)), beacons) for beacons in scanners]
    scanners = [list(beacons) for beacons in scanners]
    known_beacons = set(scanners[0])
    unknown_beacons = deque(scanners[1:])
    return known_beacons, unknown_beacons


def get_input_file_name():
    return argv[1] if len(argv) == 2 else DEFAULT_INPUT_FILE_NAME


def part1(known_beacons, unknown_beacons):
    print("Running part 1...")
    scanner_locations = [(0, 0, 0)]  # Aligning everything to the first scanner
    while len(unknown_beacons) > 0:
        distance_vector, beacons = align(known_beacons, next(iter(unknown_beacons)))
        if distance_vector and beacons:
            scanner_locations.append(distance_vector)
            known_beacons.update(beacons)
            unknown_beacons.popleft()
        else:
            unknown_beacons.rotate()
    print(f"Number of beacons: {len(known_beacons)}")
    print()
    return scanner_locations


def align(known_beacons, unknown_beacons):
    transformed_beacons = [generate_transformations(beacon) for beacon in unknown_beacons]
    for transformation in range(len(TRANSFORMATIONS)):
        beacons = [beacon[transformation] for beacon in transformed_beacons]
        distances = calculate_distances(known_beacons, beacons)
        vector, distance = Counter(distances).most_common()[0]
        if distance >= EXPECTED_OVERLAPPING_BEACONS:
            return vector, [shift_point(beacon, vector) for beacon in beacons]
    return None, None


def generate_transformations(beacon):
    return [
        tuple(beacon[axis] * rotation for axis, rotation in zip(*transformation))
        for transformation in TRANSFORMATIONS
    ]


def calculate_distances(source_beacons, target_beacons):
    return [
        distance_vector(target_beacon, source_beacon)
        for source_beacon, target_beacon in product(source_beacons, target_beacons)
    ]


def shift_point(point, vector):
    return tuple(source + target for source, target in zip(point, vector))


def distance_vector(source, target):
    return tuple(target_coord - source_coord for source_coord, target_coord in zip(source, target))


def part2(scanner_locations):
    print("Running part 2...")
    scanners_range = range(len(scanner_locations))
    scanners_distances = [
        sum(distance_vector(scanner_locations[first], scanner_locations[second]))
        for first, second in set(product(scanners_range, scanners_range))
        if first != second
    ]
    print(f"Largest Manhattan distance: {max(scanners_distances)}")
    print()


known_beacons, unknown_beacons = load_scanner_data()
scanner_locations = part1(known_beacons, unknown_beacons)
part2(scanner_locations)
