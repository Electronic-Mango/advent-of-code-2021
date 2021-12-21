"""
I've solved this task using pen & paper rather than algorithms & programming.
This script was used just to sum everything up.
I'll look into a "proper" solution for this task later on.
"""

AMPHIPODS_ENERGY_COST = {
    "A": 1,
    "B": 10,
    "C": 100,
    "D": 1000
}


def task(moves, part):
    print(f"Running part {part}...")
    energy_costs = [AMPHIPODS_ENERGY_COST[amphipod] * length for amphipod, length in moves.items()]
    total_energy_cost = sum(energy_costs)
    print(f"Total energy cost: {total_energy_cost}")
    print()


# Solved using pen & paper
part_1_moves = {
    "A": 2 + 5 + 3 + 8,
    "B": 2 + 3 + 4,
    "C": 5 + 3 + 7,
    "D": 5 + 5
}
task(part_1_moves, part=1)

# Solved using pen & paper
part_2_moves = {
    "A": 11 + 11 + 6 + 8 + 8,
    "B": 3 + 6 + 2 + 6 + 5 + 6 + 6 + 7,
    "C": 5 + 8 + 7 + 5 + 6 + 7 + 5,
    "D": 10 + 10 + 5 + 5 + 5 + 7,
}
task(part_2_moves, part=2)
