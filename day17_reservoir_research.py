from typing import List, NamedTuple, Tuple, Dict
import enum
import re

RAW = """x=495, y=2..7
y=7, x=495..501
x=501, y=3..7
x=498, y=2..4
x=506, y=1..2
x=498, y=10..13
x=504, y=10..13
y=13, x=498..504"""

XY = Tuple[int, int]

rgx = r"([xy])=([0-9]+), ([xy])=([0-9]+)..([0-9]+)"

Grid = Dict[XY, str]

def make_grid(raw: str) -> Grid:
    grid = {}
    for line in raw.split("\n"):
        first, coord, second, lo, hi = re.match(rgx, line.strip()).groups()
        if first == "x":
            x = int(coord)
            for y in range(int(lo), int(hi) + 1):
                grid[(x, y)] = '#'
        else:
            y = int(coord)
            for x in range(int(lo), int(hi) + 1):
                grid[(x, y)] = '#'

    return grid

GRID = make_grid(RAW)

def show(grid: Grid) -> str:
    x_lo = min(x for x, y in grid.keys())
    x_hi = max(x for x, y in grid.keys())
    y_lo = min(y for x, y in grid.keys())
    y_hi = max(y for x, y in grid.keys())

    rows = [[grid.get((x, y), '.') for x in range(x_lo, x_hi + 1)]
            for y in range(y_lo, y_hi + 1)]

    return "\n".join(''.join(row) + f" {y}" for y, row in enumerate(rows))

def flow(grid: Grid) -> None:
    x_lo = min(x for x, y in grid.keys())
    x_hi = max(x for x, y in grid.keys())
    y_lo = min(y for x, y in grid.keys())
    y_hi = max(y for x, y in grid.keys())

    # [-1, 1, 0] is directions to explore: left, right, down
    frontier = [(500, y_lo)]
    grid[(500, y_lo)] = 'w'

    while frontier:
        x, y = frontier.pop()
        print(x, y)
        #print(show(grid))
        #print()

        if y > y_hi or y < y_lo:
            continue

        below = (x, y + 1)
        # empty below me and on the grid
        if not below in grid and y < y_hi:
            # call me "w"
            grid[(x, y)] = 'w'
            # explore below me
            frontier.append((x, y))
            frontier.append(below)
            continue
        # empty below me, but off the grid
        elif not below in grid:
            grid[(x, y)] = 'o'
            continue
        # otherwise, there's something below me
        below_me = grid[below]

        if below_me == 'o':  # off the grid
            # then I'm off the grid too
            grid[(x, y)] = 'o'
            continue

        # also if it's adjacent to o
        adjacent_to_o = False
        x2 = x + 1
        while grid.get((x2, y)) in ('o', 'w'):
            if grid[(x2, y)] == 'o':
                adjacent_to_o = True
                break
            x2 += 1
        x2 = x - 1
        while grid.get((x2, y)) in ('o', 'w'):
            if grid[(x2, y)] == 'o':
                adjacent_to_o = True
                break
            x2 -= 1

        if adjacent_to_o:
            # then I'm off the grid too
            grid[(x, y)] = 'o'
        else:
           grid[(x, y)] = 'w'

        # there's something below me, and it's not off the grid,
        # so I need to explore left and right, maybe
        # set me to w

        left = (x - 1, y)
        right = (x + 1, y)


        # if grid.get(left) == 'o' or grid.get(right) == 'o':
        #     grid[(x, y)] = 'o'

        #     continue

        if left in grid and right in grid:
            continue

        # could go left or right or both
        # put myself back on the frontier
        frontier.append((x, y))

        if not left in grid:
            frontier.append(left)
            grid[left] = 'w'
        if not right in grid:
            frontier.append(right)
            grid[right] = 'w'

def count_water(grid: Grid) -> int:
    return len([v for v in grid.values() if v in ['w', 'o']])

flow(GRID)
assert count_water(GRID) == 57

with open('data/day17.txt') as f:
    raw = f.read().strip()

grid = make_grid(raw)
flow(grid)
print(count_water(grid))

def retained(grid: Grid) -> set:
    retained_locs = set()

    while True:
        try:
            x, y = next(xy for xy, c in grid.items() if c == 'w')

            keep = True
            accumulator = [(x, y)]

            x2 = x + 1
            while grid.get((x2, y)):
                c = grid[(x2, y)]
                if c == 'w':
                    accumulator.append((x2, y))
                    x2 += 1
                elif c == '#':  # it's a wall
                    break
                else:
                    # must be w
                    keep = False
                    break

            x2 = x - 1
            while grid.get((x2, y)):
                c = grid[(x2, y)]
                if c == 'w':
                    accumulator.append((x2, y))
                    x2 -= 1
                elif c == '#':  # it's a wall
                    break
                else:
                    # must be w
                    keep = False
                    break

            if keep:
                for loc in accumulator:
                    retained_locs.add(loc)

            for loc in accumulator:
                grid[loc] = '$'

        except StopIteration:
            return retained_locs

assert len(retained(GRID)) == 29

print(len(retained(grid)))
