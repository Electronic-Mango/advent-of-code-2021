from itertools import product
from numpy import array, full, ndindex, pad, unique
from os import linesep
from sys import argv

DEFAULT_INPUT_FILE_NAME = "input"
LIGHT_PIXEL_INITIAL = "#"
LIGHT_PIXEL = "1"
DARK_PIXEL_INITIAL = "."
DARK_PIXEL = "0"
PIXEL_MASK_INDEXES = list(product((-1, 0, 1), repeat=2))


def load_image_data():
    with open(get_input_file_name()) as input_file:
        algorithm, image = input_file.read().strip().split(linesep + linesep)
    algorithm = make_pixels_numeric(algorithm.strip())
    image = [make_pixels_numeric(line.strip()) for line in image.splitlines()]
    image = [list(line) for line in image]
    image = array(image)
    return algorithm, image


def make_pixels_numeric(pixels):
    return pixels.replace(DARK_PIXEL_INITIAL, DARK_PIXEL).replace(LIGHT_PIXEL_INITIAL, LIGHT_PIXEL)


def get_input_file_name():
    return argv[1] if len(argv) == 2 else DEFAULT_INPUT_FILE_NAME


def task(algorithm, image, number_of_iterations):
    print(f"Running task for {number_of_iterations} iterations...")
    possible_outer_pixels = ["0", algorithm[0]]
    for iteration in range(number_of_iterations):
        outer_pixel = possible_outer_pixels[iteration % len(possible_outer_pixels)]
        image = pad(image, ((1, 1), (1, 1)), constant_values=outer_pixel)
        image = process_image(image, outer_pixel)
        light_pixel_count = get_pixel_count(image, LIGHT_PIXEL)
    print(f"Number of light pixels: {light_pixel_count}")
    print()


def process_image(image, outer_pixel):
    new_image = full(image.shape, fill_value=outer_pixel)
    for indexes in ndindex(image.shape):
        value = calculate_pixel_mask_value(*indexes, image, outer_pixel)
        new_image[indexes] = algorithm[value]
    return new_image


def calculate_pixel_mask_value(x, y, image, outer_pixel):
    value = [get_pixel_value(x + dx, y + dy, image, outer_pixel) for dx, dy in PIXEL_MASK_INDEXES]
    return int("".join(value), 2)


def get_pixel_value(x, y, image, outer_pixel):
    shape_x, shape_y = image.shape
    indexes_are_in_bounds = 0 <= x < shape_x and 0 <= y < shape_y
    return image[x][y] if indexes_are_in_bounds else outer_pixel


def get_pixel_count(image, pixel_value):
    values, counts = unique(image, return_counts=True)
    return dict(zip(values, counts))[pixel_value]


algorithm, image = load_image_data()
task(algorithm, image, number_of_iterations=2)
task(algorithm, image, number_of_iterations=50)
