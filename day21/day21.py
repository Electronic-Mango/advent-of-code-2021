from collections import Counter, defaultdict
from itertools import cycle, product
from sys import argv

DEFAULT_INPUT_FILE_NAME = "input"
REGULAR_DIE_SIDES = 100
DIRAC_DIE_SIDES = 3
ROLLS_PER_ROUND = 3
REGULAR_GAME_MAX_SCORE = 1000
DIRAC_GAME_MAX_SCORE = 21
POSSIBLE_DIRAC_ROLLS = Counter(
    sum(roll) for roll in product(range(1, DIRAC_DIE_SIDES + 1), repeat=ROLLS_PER_ROUND)
)


class Player:
    def __init__(self, position, max_score, score=0):
        self.position = position
        self.max_score = max_score
        self.score = score

    def move(self, value):
        self.position = (self.position + value - 1) % 10 + 1
        self.score += self.position

    def victory(self):
        return self.score >= self.max_score

    def copy(self):
        return Player(self.position, self.max_score, self.score)

    def __eq__(self, other):
        return (self.position, self.score) == (other.position, other.score)

    def __hash__(self):
        return hash((self.position, self.score))


class RegularDie:
    def __init__(self, sides):
        self.sides = sides
        self.cycle = cycle([side for side in range(1, REGULAR_DIE_SIDES + 1)])
        self.rolled_times = 0

    def roll(self, times):
        self.rolled_times += times
        return sum([next(self.cycle) for _ in range(times)])


def load_starting_positions():
    with open(get_input_file_name()) as input_file:
        return [int(line.split()[-1]) for line in input_file.readlines()]


def get_input_file_name():
    return argv[1] if len(argv) == 2 else DEFAULT_INPUT_FILE_NAME


def part1(starting_positions):
    print("Running part 1...")
    player_states = get_players(starting_positions, REGULAR_GAME_MAX_SCORE)
    die = RegularDie(REGULAR_DIE_SIDES)
    while not game_over(player_states):
        play_regular_game(player_states, die)
    lower_score = min(player.score for player in player_states)
    result = lower_score * die.rolled_times
    print(f"Result: {result}")
    print()


def get_players(starting_positions, max_score):
    return tuple(Player(position, max_score) for position in starting_positions)


def game_over(players):
    return any(player.victory() for player in players)


def play_regular_game(players, die):
    for player in players:
        player.move(die.roll(ROLLS_PER_ROUND))
        if player.victory():
            break


def part2(starting_positions):
    print("Running part 2...")
    ongoing_universes = {get_players(starting_positions, DIRAC_GAME_MAX_SCORE): 1}
    finished_universes = defaultdict(int)
    number_of_players = len(starting_positions)
    player_order = cycle(range(number_of_players))
    while len(ongoing_universes):
        play_dirac_game(ongoing_universes, finished_universes, next(player_order))
    game_results = dirac_game_result(finished_universes, number_of_players)
    result = max(game_results)
    print(f"Most victorious player: {result}")
    print()


def play_dirac_game(ongoing_universes: dict, finished_universes, current_player):
    next_universes = defaultdict(int)
    for state, state_count in ongoing_universes.items():
        if not game_over(state):
            update_next_universes(state, state_count, next_universes, current_player)
        else:
            finished_universes[state] += state_count
    ongoing_universes.clear()
    ongoing_universes.update(next_universes)


def update_next_universes(state, count, game_states, current_player):
    for roll, roll_count in POSSIBLE_DIRAC_ROLLS.items():
        new_state = tuple(player.copy() for player in state)
        new_state[current_player].move(roll)
        game_states[new_state] += roll_count * count


def dirac_game_result(universes, number_of_players):
    return [
        sum(count for state, count in universes.items() if state[player_number].victory())
        for player_number in range(number_of_players)
    ]


starting_positions = load_starting_positions()
part1(starting_positions)
part2(starting_positions)
