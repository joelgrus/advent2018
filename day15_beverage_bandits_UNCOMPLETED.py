from typing import Set, List, Tuple, NamedTuple, Iterator, Optional

from collections import deque
import heapq

RAW = """#######
#.G...#
#...EG#
#.#.#G#
#..G#E#
#.....#
#######"""

class Pos(NamedTuple):
    i: int
    j: int

    def adjacent(self, other: 'Pos') -> int:
        return ((abs(self.i - other.i) == 1 and self.j == other.j) or
                (abs(self.j - other.j) == 1 and self.i == other.i))

    def neighbors(self) -> Iterator['Pos']:
        i, j = self.i, self.j
        yield from [Pos(i-1, j), Pos(i+1,j), Pos(i, j-1), Pos(i, j+1)]

    def manhattan(self, other: 'Pos') -> int:
        return abs(self.i - other.i) + abs(self.j - other.j)

class Fighter:
    def __init__(self, elf: bool, pos: Pos, attack: int = 3, hp: int = 200) -> None:
        self.elf = elf
        self.attack = attack
        self.hp = hp
        self.pos = pos
        self.dead = False
        self.moved_last_time = False
        self.path_to_follow = None

    def __repr__(self) -> str:
        return f"Fighter(elf={self.elf}, pos={self.pos}, attack={self.attack}, hp={self.hp})"


    def take_turn(self, cave: 'Cave', movement_last_round: bool) -> bool:
        print(self)
        "returns whether it found enemies"
        # If no enemies, return False
        enemies = [fighter for fighter in cave.fighters
                   if fighter.elf != self.elf and not fighter.dead]
        if not enemies:
            print("no enemies")
            return False

        # Elif enemy in range, attack
        adjacent_enemies = [enemy for enemy in enemies
                            if self.pos.adjacent(enemy.pos)]

        adjacent_enemies.sort(key=lambda enemy: (enemy.hp, enemy.pos.i, enemy.pos.j))

        if adjacent_enemies:
            self.moved_last_time = True
            attackee = adjacent_enemies[0]
            print("attacking", attackee)
            attackee.hp -= self.attack
            if attackee.hp <= 0:
                attackee.dead = True
            return True  # able to do somethign

        # Else move and (maybe) attack
        if not self.moved_last_time and not movement_last_round:
            # just return, if I couldn't move last time, I can't move now
            print("unable to move")
            return True
        path_to_follow = cave.optimal_path(self)
        if path_to_follow is None:
            print("no path")
            self.moved_last_time = False
            return True
        else:
            # move
            print(path_to_follow)
            self.pos = path_to_follow[1]
            self.path_to_follow = path_to_follow[1:]
            self.moved_last_time = True
            # maybe attack

            # Elif enemy in range, attack
            adjacent_enemies = [enemy for enemy in enemies
                                if self.pos.adjacent(enemy.pos)]

            adjacent_enemies.sort(key=lambda enemy: (enemy.hp, enemy.pos.i, enemy.pos.j))

            if adjacent_enemies:
                attackee = adjacent_enemies[0]
                attackee.hp -= self.attack
                if attackee.hp <= 0:
                    attackee.dead = True

            return True  # able to do somethign


class Cave(NamedTuple):
    walls: Set[Pos]
    fighters: List[Fighter]

    last_occupied = [None]

    def optimal_path(self, fighter: Fighter) -> Optional[List[Pos]]:
        """
        return the optimal path that will put me next to an enemy
        """
        #print(f"{fighter} considering where to move to")

        enemies = [f for f in self.fighters
                   if fighter.elf != f.elf and not f.dead]

        off_limits = self.walls | {f.pos for f in self.fighters if not f.dead}

        # These are the places I would like to get to
        targets = {pos
                   for enemy in enemies
                   for pos in enemy.pos.neighbors()
                   if pos not in off_limits}

        if not targets:
            # no targets
            return None

        visited = set()
        not_visited = {fighter.pos}
        came_from = {}

        # For each node, the cost of getting from the start node to that node.
        g_score = {}  # deafult iinfinity
        g_score[pos] = 0

        # or each node, the total cost of getting from the start node to the goal
        f_score  = {}  # deault infinity
        f_score[pos] = min(fighter.pos.manhattan(target) for target in targets)

        while not_visited:
            current = min(not_visited, key=lambda pos: f_score.get(pos, float('inf')))
            if current in targets:
                pass

            visited.add(pos)
            not_visited.remove(pos)



        for each neighbor of current
            if neighbor in closedSet
                continue		// Ignore the neighbor which is already evaluated.

            // The distance from start to a neighbor
            tentative_gScore := gScore[current] + dist_between(current, neighbor)

            if neighbor not in openSet	// Discover a new node
                openSet.Add(neighbor)
            else if tentative_gScore >= gScore[neighbor]
                continue;

            // This path is the best until now. Record it!
            cameFrom[neighbor] := current
            gScore[neighbor] := tentative_gScore
            fScore[neighbor] := gScore[neighbor] + heuristic_cost_estimate(neighbor, goal)

        backpointers = {fighter.pos: None}
        reached = set()

        frontier = [(min(fighter.pos.manhattan(target),
                     0,
                     for target in targets), fighter.pos)]

        best_score = float('inf')

        while frontier:
            score, length, pos = heapq.heappop(frontier)

            if score > best_score:
                # The best remaining candidate is worse than
                # what we've already found, so break
                break

            if pos in targets:
                reached.add(pos)
                best_score = length

            for next_pos in pos.neighbors():
                if next_pos in off_limits:
                    continue
                if next_pos in backpointers:

                if pos in path:
                    continue
                new_path = path + [pos]
                new_score = len(new_path) + min(pos.manhattan(target) for target in targets)
                heapq.heappush(frontier, (new_score, new_path))


        # at this point, shortest_paths has all the shortest paths
        # need to sort by (1) reading order of destination (2) reading order of first step
        successful_paths.sort(key=lambda path: (path[-1].i, path[-1].j, path[1].i, path[1].j))

        if successful_paths:
            return successful_paths[0]

        else:
            #print("nowhere good to go")
            return None


    def round(self) -> bool:
        """Return true if the game is not over"""
        occupied = {f.pos: f.elf for f in self.fighters if not f.dead}
        movement_last_round = occupied != self.last_occupied[0]

        self.fighters.sort(key=lambda f: (f.pos.i, f.pos.j))

        game_over = False

        for fighter in self.fighters:
            if fighter.dead:
                continue
            found_enemies = fighter.take_turn(self, movement_last_round)
            if not found_enemies:
                game_over = True

        self.last_occupied[0] = occupied

        return game_over

    def total_hit_points(self) -> int:
        return sum(f.hp for f in self.fighters if not f.dead)

    def __repr__(self) -> str:
        outputs = {**{pos: '#' for pos in self.walls},
                   **{f.pos: 'E' if f.elf else 'G' for f in self.fighters if not f.dead}}


        max_i = max(pos.i for pos in outputs)
        max_j = max(pos.j for pos in outputs)

        return "\n".join("".join(outputs.get(Pos(i, j), ".") for j in range(max_j + 1))
                         for i in range(max_i + 1))


def parse(raw: str) -> Cave:
    walls = set()
    fighters = []

    for i, row in enumerate(raw.split("\n")):
        for j, c in enumerate(row.strip()):
            if c == '#':
                walls.add(Pos(i, j))
            elif c == 'E':
                fighters.append(Fighter(elf=True, pos=Pos(i, j)))
            elif c == 'G':
                fighters.append(Fighter(elf=False, pos=Pos(i, j)))

    return Cave(walls, fighters)


def run_game(cave: Cave) -> int:
    num_rounds = 0
    while True:
        print("round", num_rounds)
        print(cave)
        game_over = cave.round()
        if game_over:
            break
        num_rounds += 1

    return num_rounds * cave.total_hit_points()


CAVE = parse(RAW)
assert run_game(CAVE) == 27730

CAVE2 = parse("""#######
#G..#E#
#E#E.E#
#G.##.#
#...#E#
#...E.#
#######""")

#assert run_game(CAVE2) == 36334

CAVE3 = parse("""#########
#G......#
#.E.#...#
#..##..G#
#...##..#
#...#...#
#.G...G.#
#.....G.#
#########""")

assert run_game(CAVE3) == 18740

with open('data/day15.txt') as f:
    raw = f.read()
    cave = parse(raw)

    print(run_game(cave))
