from collections import Counter, deque
from sys import argv

DEFAULT_INPUT_FILE_NAME = "input"
REPRODUCTION_INTERVAL = 6
NEW_FISH_REPRODUCTION_INTERVAL = REPRODUCTION_INTERVAL + 2
REPRODUCTION_STAGES = NEW_FISH_REPRODUCTION_INTERVAL + 1


def load_fish_stages():
    with open(get_input_file_name()) as input_file:
        return [int(stage) for stage in input_file.readline().strip().split(",")]


def get_input_file_name():
    return argv[1] if len(argv) == 2 else DEFAULT_INPUT_FILE_NAME


def simulate_fish(fish_list, number_of_days, part_number):
    print(f"Running part {part_number}...")
    fish_stages = generate_fish_stages_deque(fish_list)
    for _ in range(number_of_days):
        fish_stages.rotate(-1)
        fish_stages[REPRODUCTION_INTERVAL] += fish_stages[NEW_FISH_REPRODUCTION_INTERVAL]
    total_fish_count = sum(fish_stages)
    print(f"Total number of fish after {number_of_days} days: {total_fish_count}")
    print()


def generate_fish_stages_deque(fish_list):
    fish_stages_counter = Counter(fish_list)
    fish_stages = [fish_stages_counter.get(stage, 0) for stage in range(REPRODUCTION_STAGES)]
    return deque(fish_stages)


fish_stages_list = load_fish_stages()
simulate_fish(fish_stages_list, number_of_days=80, part_number=1)
simulate_fish(fish_stages_list, number_of_days=256, part_number=2)
