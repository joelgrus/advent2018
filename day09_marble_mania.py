from typing import List

def play_marbles_old(num_players: int, highest_marble: int) -> List[int]:
    scores = [0 for _ in range(num_players)]

    marbles = [0]
    curr = 0   # index of the current marble
    next_player = 0

    for marble in range(1, highest_marble + 1):
        if marble % 23 == 0:
            scores[next_player] += marble
            curr = (curr - 7) % len(marbles)
            scores[next_player] += marbles[curr]
            marbles = marbles[:curr] + marbles[curr+1:]
            # If we just removed the last marble, go back to 0
            curr = curr % len(marbles)
        else:
            insert_after = (curr + 1) % len(marbles)
            curr = insert_after + 1
            if insert_after == len(marbles) - 1:
                marbles.append(marble)
            else:
                marbles = marbles[:insert_after+1] + [marble] + marbles[insert_after+1:]

        next_player = (next_player + 1) % num_players

    return scores


from collections import deque

# v
# 2 3 4 1 0
#
# move left
# v
# 0 2 3 4 1
# pop() -> appendleft()

# move right
# v
# 3 4 1 0 2
# popleft() -> append()

def play_marbles(num_players: int, highest_marble: int) -> List[int]:
    scores = [0 for _ in range(num_players)]

    # current is always in position 0
    marbles = deque([0])
    next_player = 0

    def move_left(n: int = 1) -> None:
        for _ in range(n):
            val = marbles.pop()
            marbles.appendleft(val)

    def move_right(n: int = 1) -> None:
        for _ in range(n):
            val = marbles.popleft()
            marbles.append(val)

    for marble in range(1, highest_marble + 1):
        if marble % 23 == 0:
            scores[next_player] += marble

            move_left(7)
            scores[next_player] += marbles.popleft()
        else:
            # -> a -> b
            move_right(2)
            # insert between a and b
            marbles.appendleft(marble)

        next_player = (next_player + 1) % num_players

    return scores



assert max(play_marbles(9, 25)) == 32
assert max(play_marbles(10, 1618)) == 8317
assert max(play_marbles(13, 7999)) == 146373
assert max(play_marbles(17, 1104)) == 2764
assert max(play_marbles(21, 6111)) == 54718
assert max(play_marbles(30, 5807)) == 37305

#print(max(play_marbles(447, 71510)))

print(max(play_marbles(447, 7151000)))
