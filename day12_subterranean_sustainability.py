from typing import Set, Tuple
import re

State = Set[int]

Rule = Tuple[bool, bool, bool, bool, bool]
Rules = Set[Rule]

RAW = """initial state: #..#.#..##......###...###

...## => #
..#.. => #
.#... => #
.#.#. => #
.#.## => #
.##.. => #
.#### => #
#.#.# => #
#.### => #
##.#. => #
##.## => #
###.. => #
###.# => #
####. => #"""

def parse(raw: str) -> Tuple[State, Rules]:
    lines = raw.split("\n")
    rgx = "initial state: (.*)"
    initial_state_raw = re.match(rgx, lines[0]).groups()[0]
    initial_state = {i for i, plant in enumerate(initial_state_raw) if plant == '#'}

    rules = set()
    for line in lines[2:]:
        rgx = "(.....) => (.)"
        pattern, plant = re.match(rgx, line).groups()
        if plant == '#':
            key = tuple([c == '#' for c in pattern])
            rules.add(key)

    return initial_state, rules

STATE, RULES = parse(RAW)

def step(state: State, rules: Rules) -> State:
    next_state = set()

    lo = min(state) - 2
    hi = max(state) + 2

    for plant in range(lo, hi + 1):
        key = tuple([other in state
                     for other in [plant - 2, plant - 1, plant, plant + 1, plant + 2]])
        if key in rules:
            next_state.add(plant)

    return next_state

def count_plants(state: State, rules: Rules, num_generations: int) -> int:
    for _ in range(num_generations):
        state = step(state, rules)

    return sum(state)

assert count_plants(STATE, RULES, 20) == 325

with open('data/day12.txt') as f:
    raw = f.read().strip()

state, rules = parse(raw)

#print(count_plants(state, rules, 20))

seen = {}  # deltas => (generation number, lowest)
generation = 0
for generation in range(201):
    lowest = min(state)
    deltas = [plant - lowest for plant in state]
    key = tuple(sorted(deltas))
    print(generation, lowest, sum(state), key)

    if key in seen:
        print(seen[key], generation)
    else:
        seen[key] = (generation, lowest)

    state = step(state, rules)
    generation += 1

# In [34]: 9568 + 42 * (50_000_000_000 - 200)
# Out[34]: 2100000001168
