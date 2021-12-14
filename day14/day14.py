from collections import Counter, defaultdict
from math import ceil
from os import linesep
from sys import argv

DEFAULT_INPUT_FILE_NAME = "input"


def load_polymer_formula():
    with open(get_input_file_name()) as input_file:
        starting_polymer, pair_insertions = (input_file.read().strip().split(linesep + linesep))
    pair_insertions = [line.strip().split(" -> ") for line in pair_insertions.splitlines()]
    pair_insertions = {pair: new for pair, new in pair_insertions}
    return starting_polymer, pair_insertions


def get_input_file_name():
    return argv[1] if len(argv) == 2 else DEFAULT_INPUT_FILE_NAME


def task(starting_polymer, pair_insertions, steps):
    print(f"Running task with {steps} steps...")
    element_pairs = split_polymer_into_element_pairs(starting_polymer)
    element_pairs_counter = Counter(element_pairs)
    for _ in range(steps):
        polymer_modification = get_polymer_modification(element_pairs_counter, pair_insertions)
        for element_pair, occurences in polymer_modification.items():
            element_pairs_counter[element_pair] += occurences
    single_element_occurences = get_single_element_occurences(element_pairs_counter)
    result = single_element_occurences[0] - single_element_occurences[-1]
    print(f"Final result: {result}")
    print()


def split_polymer_into_element_pairs(polymer):
    return [polymer[element : element + 2] for element in range(len(starting_polymer) - 1)]


def get_polymer_modification(element_pairs_counter, pair_insertions):
    elements_modification = defaultdict(int)
    for element_pair in element_pairs_counter.keys():
        pair_occurences = element_pairs_counter[element_pair]
        new_element = pair_insertions[element_pair]
        elements_modification[element_pair[0] + new_element] += pair_occurences
        elements_modification[new_element + element_pair[1]] += pair_occurences
        elements_modification[element_pair] -= pair_occurences
    return elements_modification


def get_single_element_occurences(element_pairs_counter):
    element_counter = Counter()
    for elements_pair, ocurrences in element_pairs_counter.items():
        element_counter[elements_pair[0]] += ocurrences
        element_counter[elements_pair[1]] += ocurrences
    # All occurences are divided by 2, since most pairs of elements overlap.
    # Occurences are rounded up, since first and last elements don't overlap with anything.
    return [ceil(ocurrences / 2) for _, ocurrences in element_counter.most_common()]


starting_polymer, pair_insertions = load_polymer_formula()
task(starting_polymer, pair_insertions, steps=10)
task(starting_polymer, pair_insertions, steps=40)
