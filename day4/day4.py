from numpy import all, array, ndarray
from sys import argv

DEFAULT_INPUT_FILE_NAME = "input"
MARKED_NUMBER = "X"


def get_input_file_name():
    return argv[1] if len(argv) == 2 else DEFAULT_INPUT_FILE_NAME


def load_bingo():
    with open(get_input_file_name()) as input_file:
        input_lines = [line.strip() for line in input_file.readlines() if line.strip()]
    chosen_numbers = [number for number in input_lines.pop(0).split(",")]
    bingo_cards = [line.split() for line in input_lines]
    bingo_cards = [bingo_cards[line : line + 5] for line in range(0, len(bingo_cards), 5)]
    bingo_cards = [array(bingo_card) for bingo_card in bingo_cards]
    return chosen_numbers, bingo_cards


def part1(chosen_numbers, bingo_cards):
    print("Running part 1...")
    victor, final_number = win_at_bingo(chosen_numbers, bingo_cards)
    victor_value = get_bingo_card_value(victor) * final_number
    print("Victor value: {}".format(victor_value))
    print()


def part2(chosen_numbers, bingo_cards):
    print("Running part 2...")
    last_victor, last_number = lose_at_bingo(chosen_numbers, bingo_cards)
    last_victor_value = get_bingo_card_value(last_victor) * last_number
    print("'Victor' value: {}".format(last_victor_value))
    print()


def win_at_bingo(chosen_numbers, bingo_cards):
    for number in chosen_numbers:
        for bingo_card in bingo_cards:
            mark_card(number, bingo_card)
            if bingo_card_won(bingo_card):
                return bingo_card, int(number)


def mark_card(number, bingo_card):
    bingo_card[bingo_card == number] = MARKED_NUMBER


def bingo_card_won(bingo_card):
    any_full_column_marked = any(all(bingo_card == MARKED_NUMBER, axis=0))
    any_full_row_marked = any(all(bingo_card == MARKED_NUMBER, axis=1))
    return any_full_column_marked or any_full_row_marked


def get_bingo_card_value(bingo_card):
    return sum([int(value) for value in bingo_card.flatten() if value != MARKED_NUMBER])


def lose_at_bingo(chosen_numbers, bingo_cards):
    for number in chosen_numbers:
        for bingo_card in bingo_cards.copy():
            mark_card(number, bingo_card)
            if bingo_card_won(bingo_card):
                last_victor = bingo_card
                last_number = int(number)
                bingo_cards = [card for card in bingo_cards if not (card == last_victor).all()]
    return last_victor, last_number


chosen_numbers, bingo_cards = load_bingo()
part1(chosen_numbers, bingo_cards)
part2(chosen_numbers, bingo_cards)
