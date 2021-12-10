from numpy import array, ndindex, pad, prod
from sys import argv

DEFAULT_INPUT_FILE_NAME = "input"
MAX_HEIGHT = 9


def load_heightmap():
    with open(get_input_file_name()) as input_file:
        heightmap = [heights.strip() for heights in input_file.readlines()]
    heightmap = [list(heights) for heights in heightmap]
    heightmap = [map(int, heights) for heights in heightmap]
    heightmap = [list(heights) for heights in heightmap]
    heightmap = array(heightmap)
    return heightmap


def get_input_file_name():
    return argv[1] if len(argv) == 2 else DEFAULT_INPUT_FILE_NAME


def part1(heightmap):
    print("Running part 1...")
    minima = [(x, y) for x, y in ndindex(heightmap.shape) if is_local_minimum(x, y, heightmap)]
    risk_levels = [heightmap[x][y] + 1 for x, y in minima]
    total_risk_level = sum(risk_levels)
    print(f"Total risk level: {total_risk_level}")
    print()
    return minima


def is_local_minimum(x, y, heightmap):
    height = heightmap[x][y]
    if height == MAX_HEIGHT:
        return False
    adjacent_points = get_adjacent_points(x, y, heightmap)
    return all(height < adjacent_value for adjacent_value in adjacent_points)


def get_adjacent_points(x, y, heightmap):
    return [heightmap[x + dx][y + dy] for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]]


def part2(heightmap, height_minima):
    print("Running part 2...")
    basin_sizes = [get_basin_size(x, y, heightmap) for x, y in height_minima]
    basin_sizes.sort()
    largest_basin_sizes = basin_sizes[-3:]
    largest_basin_sizes_product = prod(largest_basin_sizes)
    print(f"Total basin size product: {largest_basin_sizes_product}")
    print()


def get_basin_size(x, y, heightmap, basin_points=set()):
    if heightmap[x][y] == MAX_HEIGHT or (x, y) in basin_points:
        return 0
    basin_points.add((x, y))
    adjacent_basin_sizes = [
        get_basin_size(x + dx, y + dy, heightmap, basin_points)
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]
    ]
    return sum(adjacent_basin_sizes) + 1  # + 1 to include this point in basin


heightmap = load_heightmap()
# Surrounding heightmap with "peaks" is a simple way of handling values along the edges
padded_heightmap = pad(heightmap, [(1, 1), (1, 1)], constant_values=MAX_HEIGHT)
height_minima = part1(padded_heightmap)
part2(padded_heightmap, height_minima)
