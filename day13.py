import json
from functools import cmp_to_key

import aoc

data = aoc.getInputForDay(13)
# data = aoc.getInputForDay(13, force_filepath="inputs/day13_example.txt")

pairs = [p.split("\n") for p in data.split("\n\n")]

# Parse JSON
for p in pairs:
    p[0] = json.loads(p[0])
    p[1] = json.loads(p[1])

RIGHT_ORDER = "RIGHT_ORDER"
FALSE_ORDER = "FALSE_ORDER"
CONTINUE = "CONTINUE"

DEBUG_LOG = False


def comparePackets(p1, p2):
    if DEBUG_LOG:
        print("")
        print("comparePackets")
        print(p1, type(p1))
        print(p2, type(p2))
    if isinstance(p1, int) and isinstance(p2, int):
        if p1 == p2:
            return CONTINUE
        if p1 < p2:
            return RIGHT_ORDER
        if p1 > p2:
            return FALSE_ORDER

    if isinstance(p1, int) and isinstance(p2, list):
        return comparePackets([p1], p2)
    if isinstance(p1, list) and isinstance(p2, int):
        return comparePackets(p1, [p2])

    assert isinstance(p1, list) and isinstance(p2, list)
    for item1, item2 in zip(p1, p2):
        result = comparePackets(item1, item2)
        assert result in [RIGHT_ORDER, FALSE_ORDER, CONTINUE]
        if result is not CONTINUE:
            return result
    # If we reach this point, the item comparison couldn't decide the list
    # => the result depends on the list size
    if len(p1) == len(p2):
        return CONTINUE
    return RIGHT_ORDER if len(p1) < len(p2) else FALSE_ORDER


accPart1 = 0
for pairIdx, pair in enumerate(pairs):
    result = comparePackets(pair[0], pair[1])

    if result == RIGHT_ORDER:
        accPart1 += pairIdx + 1

print("Part 1", accPart1)

# For Part 2, we need to sort the packets

# First flatten the array and add the new divider packets
flattenPackets = []
DIVIDER_PACKET_1 = [[2]]
DIVIDER_PACKET_2 = [[6]]
for p in pairs:
    flattenPackets.append(p[0])
    flattenPackets.append(p[1])
flattenPackets.append(DIVIDER_PACKET_1)
flattenPackets.append(DIVIDER_PACKET_2)


# Define a helper function to match comparePackets to the cmp keyword
def packetSort(p1, p2):
    result = comparePackets(p1, p2)
    if result == RIGHT_ORDER:
        return -1
    elif result == CONTINUE:
        return 0
    assert result == FALSE_ORDER
    return 1


# We need to use cmp_to_key because Python 3 removed cmp
sortedPackets = sorted(flattenPackets, key=cmp_to_key(packetSort))

index1 = sortedPackets.index(DIVIDER_PACKET_1) + 1
index2 = sortedPackets.index(DIVIDER_PACKET_2) + 1

print("Part 2", index1 * index2)
