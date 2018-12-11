from typing import Tuple

def power_level(x: int, y: int, gsn: int) -> int:
    """
    Find the fuel cell's rack ID, which is its X coordinate plus 10.
    Begin with a power level of the rack ID times the Y coordinate.
    Increase the power level by the value of the grid serial number (your puzzle input).
    Set the power level to itself multiplied by the rack ID.
    Keep only the hundreds digit of the power level (so 12345 becomes 3; numbers with no hundreds digit become 0).
    Subtract 5 from the power level.
    """
    rack_id = x + 10
    power = rack_id * y
    power += gsn
    power *= rack_id

    # keep only the hundreds digit
    power = (power // 100) % 10
    power -= 5

    return power


assert power_level(3, 5, 8) == 4
assert power_level(122, 79, 57) == -5
assert power_level(217, 196, 39) == 0
assert power_level(101, 153, 71) == 4

def find_best(gsn: int) -> Tuple[int, int]:
    power_levels = [[power_level(x, y, gsn) for y in range(300)]
                    for x in range(300)]

    return max(((x, y) for x in range(298) for y in range(298)),
               key=lambda pair: sum(power_levels[pair[0] + i][pair[1] + j]
                                    for i in range(3) for j in range(3)))

#assert find_best(18) == (33, 45)
#assert find_best(42) == (21, 61)

#print(find_best(2187))

def find_best2(gsn: int) -> Tuple[int, int]:
    best = None
    best_value = float('-inf')

    power_levels = [[power_level(x, y, gsn) for y in range(300)]
                    for x in range(300)]

    results = {(x, y, 1): power_levels[x][y]
               for x in range(300)
               for y in range(300)}

    # (1, 1)  (2, 1)  (3, 1)
    # (1, 2)  (2, 2)  (3, 2)
    # (1, 3)  (2, 3)  (3, 3)

    for s in range(2, 301):
        print(s)
        for x in range(300 - s + 1):
            for y in range(300 - s + 1):
                power = results[(x, y, s - 1)]

                for i in range(s-1):
                    power += power_levels[x + s - 1][y + i]
                    power += power_levels[x + i][y + s - 1]
                power += power_levels[x + s - 1][y + s - 1]
                results[(x, y, s)] = power

                if power > best_value:
                    best = (x, y, s)
                    best_value = power
                    print(x, y, s, power)

    return max(results.keys(), key=lambda k: results[k])

find_best2(2187)



def find_best3(gsn: int) -> Tuple[int, int]:
    best = None
    best_value = float('-inf')

    power_levels = [[power_level(x, y, gsn) for y in range(300)]
                    for x in range(300)]

    results = {(x, y, 1): power_levels[x][y]
               for x in range(300)
               for y in range(300)}

    # (1, 1)  (2, 1)  (3, 1)
    # (1, 2)  (2, 2)  (3, 2)
    # (1, 3)  (2, 3)  (3, 3)

    for s in range(2, 301):
        print(s)
        for x in range(300 - s + 1):
            for y in range(300 - s + 1):
                power = results[(x, y, s - 1)]

                for i in range(s-1):
                    power += power_levels[x + s - 1][y + i]
                    power += power_levels[x + i][y + s - 1]
                power += power_levels[x + s - 1][y + s - 1]
                results[(x, y, s)] = power

                if power > best_value:
                    best = (x, y, s)
                    best_value = power
                    print(x, y, s, power)

    return max(results.keys(), key=lambda k: results[k])



