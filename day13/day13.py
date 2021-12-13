from numpy import full
from os import linesep
from sys import argv

DEFAULT_INPUT_FILE_NAME = "input"


def load_thermal_camera_instructions():
    with open(get_input_file_name()) as input_file:
        dots_input, folds_input = input_file.read().strip().split(linesep + linesep)
    dots = parse_dots(dots_input)
    folds = parse_folds(folds_input)
    return dots, folds


def get_input_file_name():
    return argv[1] if len(argv) == 2 else DEFAULT_INPUT_FILE_NAME


def parse_dots(dots_input):
    dots = [dot.strip().split(",") for dot in dots_input.splitlines()]
    dots = [map(int, dot) for dot in dots]
    dots = [tuple(dot) for dot in dots]
    return set(dots)


def parse_folds(folds_input):
    folds = [fold.strip().split()[-1] for fold in folds_input.splitlines()]
    folds = [fold.split("=") for fold in folds]
    folds = [(axis, int(value)) for axis, value in folds]
    return [(value, 0) if axis == "x" else (0, value) for axis, value in folds]


def task(dots, folds):
    print(f"Running part 1 & 2...")
    for fold in folds:
        dots = set(fold_dot(*dot, *fold) for dot in dots)
        print(f"Number of dots: {len(dots)}")
    print()
    print("Full code:")
    print(fill_paper(dots))
    print()


def fold_dot(x, y, fold_x, fold_y):
    folded_x = 2 * fold_x - x if x > fold_x else x
    folded_y = 2 * fold_y - y if y > fold_y else y
    return abs(folded_x), abs(folded_y)


def fill_paper(dots):
    size_x = max(x for x, _ in dots) + 1
    size_y = max(y for _, y in dots) + 1
    paper = full((size_x, size_y), " ")
    for dot in dots:
        paper[dot] = chr(0x2588)
    paper = ["".join(line) for line in paper.T]
    return linesep.join(paper)


dots, folds = load_thermal_camera_instructions()
task(dots, folds)
