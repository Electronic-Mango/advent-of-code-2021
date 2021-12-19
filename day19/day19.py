from collections import Counter, deque
from itertools import product
from os import linesep
from sys import argv

DEFAULT_INPUT_FILE_NAME = "input"
EXPECTED_OVERLAPPING_BEACONS = 12
TRANSFORMATIONS = [
    lambda x, y, z: (x, y, z),
    lambda x, y, z: (x, z, -y),
    lambda x, y, z: (x, -y, -z),
    lambda x, y, z: (x, -z, y),
    lambda x, y, z: (-x, y, -z),
    lambda x, y, z: (-x, z, y),
    lambda x, y, z: (-x, -y, z),
    lambda x, y, z: (-x, -z, -y),
    lambda x, y, z: (y, x, -z),
    lambda x, y, z: (y, z, x),
    lambda x, y, z: (y, -x, z),
    lambda x, y, z: (y, -z, -x),
    lambda x, y, z: (-y, x, z),
    lambda x, y, z: (-y, z, -x),
    lambda x, y, z: (-y, -x, -z),
    lambda x, y, z: (-y, -z, x),
    lambda x, y, z: (z, x, y),
    lambda x, y, z: (z, y, -x),
    lambda x, y, z: (z, -x, -y),
    lambda x, y, z: (z, -y, x),
    lambda x, y, z: (-z, x, -y),
    lambda x, y, z: (-z, y, x),
    lambda x, y, z: (-z, -x, y),
    lambda x, y, z: (-z, -y, -x),
]
# Surely, there's a better way of doing this...


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
    for transformation in TRANSFORMATIONS:
        beacons, vector, distance = transform(transformation, known_beacons, unknown_beacons)
        if distance >= EXPECTED_OVERLAPPING_BEACONS:
            shifted_beacons = [shift_point(beacon, vector) for beacon in beacons]
            return vector, shifted_beacons
    return None, None


def transform(transformation, known_beacons, unknown_beacons):
    transformed_unknown_beacons = [transformation(*beacon) for beacon in unknown_beacons]
    distances = [
        distance_vector(unknown_beacon, known_beacon)
        for known_beacon, unknown_beacon in product(known_beacons, transformed_unknown_beacons)
    ]
    return transformed_unknown_beacons, *Counter(distances).most_common()[0]


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
