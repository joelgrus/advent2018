RAW = """[1518-11-01 00:00] Guard #10 begins shift
[1518-11-01 00:05] falls asleep
[1518-11-01 00:25] wakes up
[1518-11-01 00:30] falls asleep
[1518-11-01 00:55] wakes up
[1518-11-01 23:58] Guard #99 begins shift
[1518-11-02 00:40] falls asleep
[1518-11-02 00:50] wakes up
[1518-11-03 00:05] Guard #10 begins shift
[1518-11-03 00:24] falls asleep
[1518-11-03 00:29] wakes up
[1518-11-04 00:02] Guard #99 begins shift
[1518-11-04 00:36] falls asleep
[1518-11-04 00:46] wakes up
[1518-11-05 00:03] Guard #99 begins shift
[1518-11-05 00:45] falls asleep
[1518-11-05 00:55] wakes up""".split("\n")

# Want to find Guard with the most minutes asleep
# Want to compute (ID of guard) * (most asleep minute)
from typing import NamedTuple, List, Tuple
import re

class Timestamp(NamedTuple):
    year: int
    month: int
    day: int
    hour: int
    minute: int

class Nap(NamedTuple):
    guard_id: int
    sleep: int    # minute at which he falls asleep
    wake: int     # minute at which he wakes up

rgx = r"\[([0-9]{4})-([0-9]{2})-([0-9]{2}) ([0-9]{2}):([0-9]{2})\] (.*)"

guard_id_rgx = r"Guard #([0-9]+) begins shift"

def find_naps(entries: List[str]) -> List[Nap]:
    naps: List[Nap] = []

    entries = sorted(entries)

    guard_id = sleep = wake = None

    for entry in entries:
        year, month, day, hour, minute, comment = re.match(rgx, entry).groups()
        ts = Timestamp(int(year), int(month), int(day), int(hour), int(minute))

        guard = re.match(guard_id_rgx, comment)

        if guard:
            assert sleep is None and wake is None
            guard_id = int(guard.groups()[0])

        elif "falls asleep" in comment:
            assert guard_id is not None and sleep is None and wake is None
            sleep = int(minute)
        elif "wakes up" in comment:
            assert guard_id is not None and sleep is not None and wake is None
            wake = int(minute)
            naps.append(Nap(guard_id, sleep, wake))
            sleep = wake = None

    return naps

NAPS = find_naps(RAW)

from collections import Counter

def sleepiest_guard(naps: List[Nap]) -> int:
    sleep_counts = Counter()

    for nap in naps:
        sleep_counts[nap.guard_id] += (nap.wake - nap.sleep)

    return sleep_counts.most_common(1)[0][0]

def most_common_sleepy_minute(naps: List[Nap], guard_id: int) -> int:
    minutes = Counter()

    for nap in naps:
        if nap.guard_id == guard_id:
            for minute in range(nap.sleep, nap.wake):
                minutes[minute] += 1

    [(minute1, count1), (minute2, count2)] = minutes.most_common(2)
    assert count1 > count2
    return minute1

assert sleepiest_guard(NAPS) == 10
assert most_common_sleepy_minute(NAPS, guard_id=10) == 24

with open('data/day04.txt') as f:
    entries = [line for line in f]
    naps = find_naps(entries)

sleepiest_guard_id = sleepiest_guard(naps)
sleepiest_minute = most_common_sleepy_minute(naps, sleepiest_guard_id)
print(sleepiest_guard_id * sleepiest_minute)

def most_frequently_asleep_minute(naps: List[Nap]) -> Tuple[int, int]:
    counts = Counter()
    for nap in naps:
        for minute in range(nap.sleep, nap.wake):
            counts[(nap.guard_id, minute)] += 1

    [((gid1, min1), count1), ((gid2, min2), count2)] = counts.most_common(2)
    assert count1 > count2

    return (gid1, min1)

assert most_frequently_asleep_minute(NAPS) == (99, 45)

guard_id, minute = most_frequently_asleep_minute(naps)
print(guard_id, minute, guard_id * minute)
