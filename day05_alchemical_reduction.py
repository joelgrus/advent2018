def same_type(s1: str, s2: str) -> bool:
    """A and a are the same type"""
    return s1.lower() == s2.lower()


# [0, 1, 2, 3, ...]


def reduct(polymer: str) -> str:
    cs = list(polymer)
    l = len(cs)-1
    i = 0

    while i<l:
        c1=cs[i]
        c2=cs[i+1]

        if same_type(c1,c2) and c1!=c2:
            del(cs[i],cs[i])
            i-=1
            l-=2
        else:
            i+=1

    return "".join(cs)


assert reduct("Aa") == ""
assert reduct("abBA") == ""
assert reduct("abAB") == "abAB"
assert reduct("aabAAB") == "aabAAB"
assert reduct("dabAcCaCBAcCcaDA") == "dabCBAcaDA"

with open('data/day05.txt') as f:
    polymer = f.read().strip()

# print(len(reduct(polymer)))

chars = {c.lower() for c in polymer}

best = {}

for c in chars:
    print(c)
    polymer_no_c = polymer.replace(c, "").replace(c.upper(), "")
    best[c] = len(reduct(polymer_no_c))

print(best)
best_key = min(best, key=lambda c: best[c])
print(best_key)
