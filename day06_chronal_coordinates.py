from typing import NamedTuple, List, Dict
from collections import Counter

class Point(NamedTuple):
    x: int
    y: int

    def manhattan_distance(self, other: 'Point') -> int:
        return abs(self.x - other.x) + abs(self.y - other.y)

    def total_manhattan_distance(self, others: List['Point']) -> int:
        return sum(self.manhattan_distance(point) for point in others)

    @staticmethod
    def from_line(line: str) -> 'Point':
        x, y = line.split(", ")
        return Point(int(x), int(y))


RAW = """1, 1
1, 6
8, 3
3, 4
5, 5
8, 9"""

LINES = RAW.split("\n")
POINTS = [Point.from_line(line) for line in LINES]

def closests(points: List[Point]) -> Dict[Point, int]:
    min_x = min(point.x for point in points)
    max_x = max(point.x for point in points)
    min_y = min(point.y for point in points)
    max_y = max(point.y for point in points)

    grid = {}

    for x in range(min_x, max_x + 1):
        for y in range(min_y, max_y + 1):
            this = Point(x, y)
            distances = [(this.manhattan_distance(point), i)
                         for i, point in enumerate(points)]
            distances.sort()
            if distances[0][0] == distances[1][0]:
                # Two closest points are equally close
                grid[this] = None
            else:
                grid[this] = distances[0][1]

    return grid

GRID = closests(POINTS)

def count_areas(grid: Dict[Point, int]) -> int:
    min_x = min(point.x for point in grid)
    max_x = max(point.x for point in grid)
    min_y = min(point.y for point in grid)
    max_y = max(point.y for point in grid)

    boundary_idxs = set()

    for point, idx in grid.items():
        if point.x in (min_x, max_x) or point.y in (min_y, max_y):
            boundary_idxs.add(idx)

    areas = Counter()

    for point, idx in grid.items():
        if idx not in boundary_idxs:
            areas[idx] += 1

    return areas

with open('data/day06.txt') as f:
    lines = [line.strip() for line in f]
    points = [Point.from_line(line) for line in lines]

# grid = closests(points)
# areas = count_areas(grid)
# print(areas)
# print(areas.most_common(1))


# Given a grid, find how many points are within some total distance.
def count_squares_within(points: List[Point], total_distance: int) -> int:
    min_x = min(point.x for point in points)
    max_x = max(point.x for point in points)
    min_y = min(point.y for point in points)
    max_y = max(point.y for point in points)

    print(min_x, max_x, min_y, max_y)


    # Need to go an extra total_distance // num_points off to the side
    delta = total_distance // len(points)

    squares = set()

    for x in range(min_x - delta, max_x + delta + 1):
        for y in range(min_y - delta, max_y + delta + 1):
            tmd = Point(x, y).total_manhattan_distance(points)

            if tmd < total_distance:
                print(x, y, tmd)
                squares.add(Point(x, y))

    return squares

# print(count_squares_within(POINTS, 32))

squares = count_squares_within(points, 10000)


# x goes 40 to 346
# y goes 53 to 351

# for x in [40, 346]:
#     for y in range(53, 352):
#         print(x, y, Point(x, y).total_manhattan_distance(points))

# for y in [53, 352]:
#     for x in range(40, 347):
#         print(x, y, Point(x, y).total_manhattan_distance(points))

# in_grid = [(x, y, Point(x, y).total_manhattan_distance(points))
#            for x in range(40, 347)
#            for y in range(53, 352)]
