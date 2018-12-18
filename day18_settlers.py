from typing import List, Iterator
from collections import Counter
import tqdm

RAW = """.#.#...|#.
.....#|##|
.|..|...#.
..|#.....#
#.#|||#|#|
...#.||...
.|....|...
||...#|.#|
|.||||..|.
...#.|..|."""

Area = List[List[str]]

def parse(raw: str) -> Area:
    return [list(line.strip()) for line in raw.split("\n")]

AREA = parse(RAW)

def next_area(area: Area) -> Area:
    nr = len(area)
    nc = len(area[0])

    def neighbors(i: int, j: int) -> Iterator[str]:
        for di in [-1, 0, 1]:
            for dj in [-1, 0, 1]:
                i2 = i + di
                j2 = j + dj

                if 0 <= i2 < nr and 0 <= j2 < nc and (i2, j2) != (i, j):
                    yield area[i2][j2]

    def next_acre(i: int, j: int) -> str:
        me = area[i][j]
        counts = Counter(neighbors(i, j))
        if me == '.':
            if counts['|'] >= 3:
                return '|'
            else:
                return '.'
        elif me == '|':
            if counts['#'] >= 3:
                return '#'
            else:
                return '|'
        elif me == '#':
            if counts['#'] > 0 and counts['|'] > 0:
                return '#'
            else:
                return '.'
        else:
            raise ValueError(f"unknown area {me}")

    return [[next_acre(i, j) for j in range(nc)] for i in range(nr)]

def resource_value(area: Area, num_minutes: int = 10) -> int:
    for _ in range(num_minutes):
        area = next_area(area)

    counts = Counter(acre for row in area for acre in row)

    return counts['#'] * counts['|']

assert resource_value(AREA, 10) == 1147

with open('data/day18.txt') as f:
    raw = f.read().strip()

area = parse(raw)
print(resource_value(area, 10))

def signature(area: Area) -> str:
    return "".join(c for row in area for c in row)

seen = {}

# for i in tqdm.trange(1000):
#     sig = signature(area)
#     if sig in seen:
#         print(i, seen[sig])
#     seen[sig] = i
#     area = next_area(area)

# 1_000_000_000 - 35 * x == 500
#  35 * x = 1_000_000_000 - 500

total = 1_000_000_000
assert (total - 510) % 35 == 0

for i in tqdm.trange(510):
    area = next_area(area)

print(resource_value(area, 0))
