from typing import NamedTuple, List, Tuple

RAW = "2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2"
INPUT = [int(x) for x in RAW.split()]

class Node(NamedTuple):
    num_children: int
    num_metadata: int
    children: List['Node']
    metadata: List[int]

"""
2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2
A----------------------------------
    B----------- C-----------
                     D-----
"""

def get_nodes(inputs: List[int], start: int = 0) -> Tuple[Node, int]:
    num_children = inputs[start]
    num_metadata = inputs[start + 1]
    start = start + 2

    children = []

    for _ in range(num_children):
        child, start = get_nodes(inputs, start)
        children.append(child)

    metadata = inputs[start:start+num_metadata]

    return Node(num_children, num_metadata, children, metadata), (start + num_metadata)

NODE, _ = get_nodes(INPUT)

def sum_all_metadata(node: Node) -> int:
    return sum(node.metadata) + sum(sum_all_metadata(child) for child in node.children)

assert sum_all_metadata(NODE) == 138

with open('data/day08.txt') as f:
    raw = f.read().strip()

inputs = [int(x) for x in raw.split()]
node, _ = get_nodes(inputs)

# print(sum_all_metadata(node))

def value(node: Node) -> int:
    if node.num_children == 0:
        return sum(node.metadata)
    else:
        child_values = {i: value(child) for i, child in enumerate(node.children)}
        return sum(child_values.get(i - 1, 0) for i in node.metadata)

assert value(NODE) == 66

print(value(node))
