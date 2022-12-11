from collections import deque
from typing import Deque, List
import math
import copy

import aoc


class Monkey(object):
    def __init__(self):
        self.currentItems: Deque[int] = deque()
        self.operator: str = "+"
        self.operationValue: str = ""
        self.testDivider: int = 1
        self.monkeyIfTrue: int = -1
        self.monkeyIfFalse: int = -1
        self.inspectionCount: int = 0


data = aoc.getInputForDay(11)
descriptions = [raw.split("\n") for raw in data.split("\n\n")]


monkeys: List[Monkey] = []
for monkeyLines in descriptions:
    monkey = Monkey()
    monkey.currentItems = deque()
    monkey.currentItems.extend(
        [int(i) for i in monkeyLines[1].split(": ")[1].split(", ")]
    )
    operator = monkeyLines[2].split("new = old ")[1][0]
    assert operator == "+" or operator == "*"
    monkey.operator = operator
    monkey.operationValue = monkeyLines[2].split(" ")[-1]
    monkey.testDivider = int(monkeyLines[3].split("divisible by ")[1])
    monkey.monkeyIfTrue = int(monkeyLines[4].split(" ")[-1])
    monkey.monkeyIfFalse = int(monkeyLines[5].split(" ")[-1])
    monkeys.append(monkey)


def simulate(isPart1: bool, monkeys: List[Monkey]):
    NB_OF_ROUNDS = 20 if isPart1 else 10000

    # Optimization:
    # Because in Part 2, the numbers get really big 🐘, we have to
    # work with modulo values which retain the expected properties
    # the modulo value is the LCM of the testDivider, or the product as their are all prime
    # (I had to look up some hints to find this logic)
    bigModulo = math.prod([m.testDivider for m in monkeys])

    for _ in range(NB_OF_ROUNDS):
        for m in monkeys:
            while len(m.currentItems) > 0:
                # Increase counter
                m.inspectionCount += 1

                # Inspect
                item = m.currentItems.popleft()
                itemPriority = None
                if m.operator == "+":
                    assert m.operationValue.isdigit()
                    itemPriority = item + int(m.operationValue)
                else:
                    assert m.operator == "*"
                    if m.operationValue == "old":
                        itemPriority = item * item
                    else:
                        assert m.operationValue.isdigit()
                        itemPriority = item * int(m.operationValue)

                if isPart1:
                    # Relief
                    itemPriority = math.floor(itemPriority / 3)
                else:
                    # Optimize
                    itemPriority %= bigModulo

                # Throw
                if itemPriority % m.testDivider == 0:
                    monkeys[m.monkeyIfTrue].currentItems.append(itemPriority)
                else:
                    monkeys[m.monkeyIfFalse].currentItems.append(itemPriority)

    mostActive = sorted([m.inspectionCount for m in monkeys])[-2:]
    return mostActive[0] * mostActive[1]


_monkeys = copy.deepcopy(monkeys)
print("Part 1", simulate(isPart1=True, monkeys=_monkeys))

_monkeys = copy.deepcopy(monkeys)
print("Part 2", simulate(isPart1=False, monkeys=_monkeys))
