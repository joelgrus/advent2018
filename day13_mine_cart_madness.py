from typing import Dict, Set, NamedTuple, Tuple, List, Optional
import enum

RAW = r"""/->-\
|   |  /----\
| /-+--+-\  |
| | |  | v  |
\-+-/  \-+--/
  \------/   """

class Pos(NamedTuple):
    x: int
    y: int

Track = Dict[Pos, str]

class Direction(enum.Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

class Turn(enum.Enum):
    LEFT = 0
    STRAIGHT = 1
    RIGHT = 2

def next_turn(turn: Turn) -> Turn:
    if turn == Turn.LEFT:
        return Turn.STRAIGHT
    elif turn == Turn.STRAIGHT:
        return Turn.RIGHT
    else:
        return Turn.LEFT

class Cart:
    def __init__(self, pos: Pos, direction: Direction) -> None:
        self.pos = pos
        self.direction = direction
        self.turn = Turn.LEFT

    def __repr__(self) -> str:
        return f"Cart({self.pos}, {self.direction})"

    def step(self, track: Track) -> None:
        x, y = self.pos
        if self.direction == Direction.UP:
            self.pos = Pos(x, y - 1)
        elif self.direction == Direction.RIGHT:
            self.pos = Pos(x + 1, y)
        elif self.direction == Direction.DOWN:
            self.pos = Pos(x, y + 1)
        else:
            self.pos = Pos(x - 1, y)

        c = track[self.pos]  # new piece of track
        if c in ['|', '-']:
            return

        elif c == '/':
            if self.direction == Direction.UP:
                self.direction = Direction.RIGHT
            elif self.direction == Direction.RIGHT:
                self.direction = Direction.UP
            elif self.direction == Direction.DOWN:
                self.direction = Direction.LEFT
            else:  # LEFT
                self.direction = Direction.DOWN

        elif c == "\\":
            if self.direction == Direction.UP:
                self.direction = Direction.LEFT
            elif self.direction == Direction.RIGHT:
                self.direction = Direction.DOWN
            elif self.direction == Direction.DOWN:
                self.direction = Direction.RIGHT
            else:  # LEFT
                self.direction = Direction.UP

        elif c == "+":
            dir_int = self.direction.value

            if self.turn == Turn.RIGHT:
                self.direction = Direction((dir_int + 1) % 4)
            elif self.turn == Turn.LEFT:
                self.direction = Direction((dir_int - 1) % 4)

            self.turn = next_turn(self.turn)

        else:
            raise ValueError(f"bad track {c}")


def parse(raw: str) -> Tuple[Track, List[Cart]]:
    track = {}
    carts = []

    lines = raw.split("\n")
    for y, line in enumerate(lines):
        for x, c in enumerate(line.rstrip()):
            pos = Pos(x, y)
            if c == ' ':
                continue
            elif c == '>':
                carts.append(Cart(pos, Direction.RIGHT))
                track[pos] = '-'
            elif c == '<':
                carts.append(Cart(pos, Direction.LEFT))
                track[pos] = '-'
            elif c == 'v':
                carts.append(Cart(pos, Direction.DOWN))
                track[pos] = '|'
            elif c == '^':
                carts.append(Cart(pos, Direction.UP))
                track[pos] = '|'
            else:
                track[pos] = c

    return track, carts

TRACK, CARTS = parse(RAW)

def tick(carts: List[Cart], track: Track) -> Optional[Pos]:
    """
    Returns None if no crash, location of first crash otherwise
    """
    carts.sort(key=lambda cart: (cart.pos.y, cart.pos.x))
    cart_locations = {cart.pos for cart in carts}

    for cart in carts:
        cart_locations.remove(cart.pos)
        cart.step(track)
        if cart.pos in cart_locations:
            return cart.pos
        cart_locations.add(cart.pos)

def first_crash(carts: List[Cart], track: Track) -> Pos:
    while True:
        crash = tick(carts, track)
        if crash is not None:
            return crash

assert first_crash(CARTS, TRACK) == Pos(7, 3)

with open('data/day13.txt') as f:
    track, carts = parse(f.read())

print(first_crash(carts, track))

def last_cart_standing(carts: List[Cart], track: Track) -> Pos:
    """
    Remove crashing carts until only one cart is left
    """
    # one loop
    while True:
        # move them in this order
        carts.sort(key=lambda cart: (cart.pos.y, cart.pos.x))

        # store: location -> cart_idx
        cart_locations = {cart.pos: i for i, cart in enumerate(carts)}

        # idxs to remove
        removed = set()

        for i, cart in enumerate(carts):
            # if already crashed this tick, skip it
            if i in removed: continue

            # unregister my location
            del cart_locations[cart.pos]

            # take a step
            cart.step(track)

            # if another cart is at the new location
            if cart.pos in cart_locations:
                # mark me for removal
                removed.add(i)
                # mark the other cart here for removal
                removed.add(cart_locations[cart.pos])
                # unregister the other cart
                del cart_locations[cart.pos]
            # otherwise, add me back at new location
            cart_locations[cart.pos] = i

        # throw out carts that were marked for removal
        carts = [cart for i, cart in enumerate(carts) if i not in removed]

        if len(carts) == 1:
            return carts[0].pos

RAW2 = r"""/>-<\
|   |
| /<+-\
| | | v
\>+</ |
  |   ^
  \<->/"""

TRACK2, CARTS2 = parse(RAW2)

assert last_cart_standing(CARTS2, TRACK2) == Pos(6, 4)

with open('data/day13.txt') as f:
    track, carts = parse(f.read())

print(last_cart_standing(carts, track))
