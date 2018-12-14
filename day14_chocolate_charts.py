from typing import List

def digits(x: int) -> List[int]:
    return [int(d) for d in str(x)]

assert digits(103) == [1, 0, 3]
assert digits(5) == [5]

def new_recipes(recipe1: int, recipe2: int) -> List[int]:
    total = recipe1 + recipe2
    return digits(total)

assert new_recipes(3, 7) == [1, 0]

def scoreboard(num_steps: int, recipe1: int = 3, recipe2: int = 7):
    scores = [recipe1, recipe2]
    elf1 = 0
    elf2 = 1

    while len(scores) < num_steps:
        scores.extend(new_recipes(scores[elf1], scores[elf2]))
        elf1 = (elf1 + scores[elf1] + 1) % len(scores)
        elf2 = (elf2 + scores[elf2] + 1) % len(scores)

    return scores

assert scoreboard(20) == [3, 7, 1, 0, 1, 0, 1, 2, 4, 5, 1, 5, 8, 9, 1, 6, 7, 7, 9, 2]

def ten_after(n: int):
    scores = scoreboard(n + 10)

    return ''.join(str(x) for x in scores[n:n+10])

assert ten_after(9) == '5158916779'
assert ten_after(18) == '9251071085'

#print(ten_after(147061))

def recipes_to_the_left(n: int, recipe1: int = 3, recipe2: int = 7) -> int:
    n_digits = digits(n)
    num_digits = len(n_digits)

    scores = [recipe1, recipe2]
    elf1 = 0
    elf2 = 1

    while True:
        for new_recipe in new_recipes(scores[elf1], scores[elf2]):
            scores.append(new_recipe)
            if scores[-num_digits:] == n_digits:
                return len(scores) - num_digits

        elf1 = (elf1 + scores[elf1] + 1) % len(scores)
        elf2 = (elf2 + scores[elf2] + 1) % len(scores)

assert recipes_to_the_left(92510) == 18
assert recipes_to_the_left(59414) == 2018

print(recipes_to_the_left(147061))
