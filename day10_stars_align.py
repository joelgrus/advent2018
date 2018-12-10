RAW = """position=< 9,  1> velocity=< 0,  2>
position=< 7,  0> velocity=<-1,  0>
position=< 3, -2> velocity=<-1,  1>
position=< 6, 10> velocity=<-2, -1>
position=< 2, -4> velocity=< 2,  2>
position=<-6, 10> velocity=< 2, -2>
position=< 1,  8> velocity=< 1, -1>
position=< 1,  7> velocity=< 1,  0>
position=<-3, 11> velocity=< 1, -2>
position=< 7,  6> velocity=<-1, -1>
position=<-2,  3> velocity=< 1,  0>
position=<-4,  3> velocity=< 2,  0>
position=<10, -3> velocity=<-1,  1>
position=< 5, 11> velocity=< 1, -2>
position=< 4,  7> velocity=< 0, -1>
position=< 8, -2> velocity=< 0,  1>
position=<15,  0> velocity=<-2,  0>
position=< 1,  6> velocity=< 1,  0>
position=< 8,  9> velocity=< 0, -1>
position=< 3,  3> velocity=<-1,  1>
position=< 0,  5> velocity=< 0, -1>
position=<-2,  2> velocity=< 2,  0>
position=< 5, -2> velocity=< 1,  2>
position=< 1,  4> velocity=< 2,  1>
position=<-2,  7> velocity=< 2, -2>
position=< 3,  6> velocity=<-1, -1>
position=< 5,  0> velocity=< 1,  0>
position=<-6,  0> velocity=< 2,  0>
position=< 5,  9> velocity=< 1, -2>
position=<14,  7> velocity=<-2,  0>
position=<-3,  6> velocity=< 2, -1>"""

from typing import List

import re
rgx = r"position=<(.*)> velocity=<(.*)>"


class Star:
    def __init__(self, x: int, y: int, dx: int, dy: int) -> None:
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy

    def __repr__(self) -> str:
        return f"Star({self.x}, {self.y}, {self.dx}, {self.dy})"

    def step(self, num_steps: int = 1) -> None:
        self.x += num_steps * self.dx
        self.y += num_steps * self.dy

    @staticmethod
    def from_line(line: str) -> 'Star':
        position, velocity = re.match(rgx, line).groups()
        x, y = [int(n) for n in position.split(",")]
        dx, dy = [int(n) for n in velocity.split(",")]
        return Star(x, y, dx, dy)

STARS = [Star.from_line(line)
         for line in RAW.split("\n")]

def show(stars: List[Star]) -> str:
    locations = set()
    for star in stars:
        locations.add((star.x, star.y))

    min_x = min(star.x for star in stars)
    max_x = max(star.x for star in stars)
    min_y = min(star.y for star in stars)
    max_y = max(star.y for star in stars)

    grid = [['#' if (x, y) in locations else '.'
             for x in range(min_x, max_x + 1)]
            for y in range(min_y, max_y + 1)]

    return "\n".join("".join(row) for row in grid)


with open('data/day10.txt') as f:
    lines = [line.strip() for line in f]

stars = [Star.from_line(line) for line in lines]

def grid_size(stars: List[Star]) -> int:
    min_x = min(star.x for star in stars)
    max_x = max(star.x for star in stars)
    min_y = min(star.y for star in stars)
    max_y = max(star.y for star in stars)

    return (max_x - min_x) * (max_y - min_y)

for star in stars:
    star.step(10391)

print(show(stars))
