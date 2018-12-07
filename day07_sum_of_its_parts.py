from typing import Tuple, List, Set, Dict, NamedTuple
import re

Req = Tuple[str, str]  # (must be finished before, can be done)

RAW = """Step C must be finished before step A can begin.
Step C must be finished before step F can begin.
Step A must be finished before step B can begin.
Step A must be finished before step D can begin.
Step B must be finished before step E can begin.
Step D must be finished before step E can begin.
Step F must be finished before step E can begin."""

LINES = RAW.split("\n")

rgx = r"Step ([A-Z]) must be finished before step ([A-Z]) can begin."

def parse_line(line: str) -> Tuple[str, str]:
    pre, post = re.match(rgx, line).groups()

    return (pre, post)

REQUIREMENTS = [parse_line(line) for line in LINES]

Preconditions = Dict[str, Set[str]]

def preconditions(requirements: List[Req]) -> Preconditions:
    steps = {step for req in requirements for step in req}

    preconds = {step: set() for step in steps}

    for pre, post in requirements:
        preconds[post].add(pre)

    return preconds


def find_order(requirements: List[Req]) -> str:
    order = []

    preconds = preconditions(requirements)

    while preconds:
        candidates = [step for step, reqs in preconds.items()
                      if not reqs]

        next_item = min(candidates)
        order.append(next_item)

        # remove that from all the preconditions
        for reqs in preconds.values():
            if next_item in reqs:
                reqs.remove(next_item)

        del preconds[next_item]

    return "".join(order)

assert find_order(REQUIREMENTS) == "CABDFE"

with open('data/day07.txt') as f:
    lines = [line.strip() for line in f]

requirements = [parse_line(line) for line in lines]
#print(find_order(requirements))


def step_time(step: str, base: int = 60) -> int:
    return ord(step) - ord('A') + 1 + base

assert step_time('A') == 61
assert step_time('Z') == 86
assert step_time('B', base=0) == 2


class WorkItem(NamedTuple):
    worker_id: int
    item: str
    start_time: int
    end_time: int


def find_time(requirements: List[Req], num_workers: int, base: int = 60) -> int:

    # { A: {B, C, D}, D: {E}}
    preconds = preconditions(requirements)

    work_items = [None for _ in range(num_workers)]

    time = 0
    while preconds or any(work_items):
        print(time, work_items)
        # Check if anyone is done, and remove those
        for i, work_item in enumerate(work_items):
            if work_item and work_item.end_time <= time:
                # This item is now finished
                work_items[i] = None

                for reqs in preconds.values():
                    if work_item.item in reqs:
                        reqs.remove(work_item.item)

        # Find available workers
        available_workers = [i for i in range(num_workers)
                             if work_items[i] is None]

        # Find candidates for work
        candidates = sorted([step for step, reqs in preconds.items()
                             if not reqs], reverse=True)

        # Assign as much work as possible
        while available_workers and candidates:
            worker_id = available_workers.pop()
            item = candidates.pop()

            work_items[worker_id] = WorkItem(
                worker_id=worker_id,
                item=item,
                start_time=time,
                end_time=time + step_time(item, base)
            )

            del preconds[item]


        if any(work_items):
            time = min(work_item.end_time
                       for work_item in work_items
                       if work_item)

    return time

# print(find_time(REQUIREMENTS, num_workers=2, base=0))

print(find_time(requirements, num_workers=5))
