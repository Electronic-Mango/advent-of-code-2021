from sys import argv

DEFAULT_INPUT_FILE_NAME = "input"
NUMBER_OF_SEGMENTS_TO_POSSIBLE_DIGITS = {
    2: (1),
    3: (7),
    4: (4),
    5: (2, 3, 5),
    6: (0, 6, 9),
    7: (8),
}


def load_entries():
    with open(get_input_file_name()) as input_file:
        return [parse_entry(entry) for entry in input_file.readlines()]


def get_input_file_name():
    return argv[1] if len(argv) == 2 else DEFAULT_INPUT_FILE_NAME


def parse_entry(entry):
    patterns = [convert_segments_to_tuples(segments) for segments in entry.split(" | ")]
    return tuple(patterns)


def convert_segments_to_tuples(segments):
    return [tuple(sorted(segment)) for segment in segments.split()]


def part1(entries):
    print("Running part 1...")
    outputs = [signal[-1] for signal in entries]
    flat_outputs = [response for response_group in outputs for response in response_group]
    unique_sizes = [
        number_of_segments
        for number_of_segments, digits in NUMBER_OF_SEGMENTS_TO_POSSIBLE_DIGITS.items()
        if type(digits) == int
    ]
    unique_outputs = [segment for segment in flat_outputs if len(segment) in unique_sizes]
    print(f"Number of unique digits: {len(unique_outputs)}")
    print()


def part2(entries):
    print("Running part 2...")
    responses = [extract_output_digits_from_entry(entry) for entry in entries]
    total_response = sum(responses)
    print(f"Total value: {total_response}")
    print()


def extract_output_digits_from_entry(entry):
    request, response = entry
    segments_to_digits = prepare_segments_to_digit_mapping(request)
    response_values = [segments_to_digits[segment] for segment in response]
    return int("".join(map(str, response_values)))


def prepare_segments_to_digit_mapping(request):
    segments_to_digits = {
        segments: NUMBER_OF_SEGMENTS_TO_POSSIBLE_DIGITS[len(segments)] for segments in request
    }
    unique_digit_to_segments_mapping = {
        digits: segment for segment, digits in segments_to_digits.items() if type(digits) == int
    }
    return {
        segments: get_digit(segments, digits, unique_digit_to_segments_mapping)
        for segments, digits in segments_to_digits.items()
    }


def get_digit(segments, digits, unique_mapping):
    if digits in unique_mapping.keys():
        return digits
    overlapping_with_4 = number_of_overlapping_elements(segments, unique_mapping[4])
    overlapping_with_7 = number_of_overlapping_elements(segments, unique_mapping[7])
    number_of_segments = len(segments)
    # Each tuple in "case" could be done programmatically, however it would require a separate
    # match-like dictionary and mapping of each digit to its segments, while this is much simpler
    match (overlapping_with_4, overlapping_with_7, number_of_segments):
        case (3, 3, 6): return 0
        case (2, 2, 5): return 2
        case (3, 3, 5): return 3
        case (3, 2, 5): return 5
        case (3, 2, 6): return 6
        case (4, 3, 6): return 9


def number_of_overlapping_elements(list1, list2):
    return len(set(list1) & set(list2))


entries = load_entries()
part1(entries)
part2(entries)
