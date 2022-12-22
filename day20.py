from copy import deepcopy
from typing import List, Optional

import aoc

data = aoc.getLinesForDay(20)
# data = aoc.getLinesForDay(20, force_filepath="inputs/day20_example.txt")

data = [int(x) for x in data]


class Node:
    def __init__(self, value: int):
        self.value: int = value
        self.prev: Optional[Node] = None
        self.next: Optional[Node] = None


def getChainFromData(data, isPart2=False):
    originalOrderNodes: List[Node] = []

    for number in data:
        value = number * (811589153 if isPart2 else 1)
        n = Node(value)
        if len(originalOrderNodes) > 0:
            prevNode = originalOrderNodes[-1]
            n.prev = prevNode
            prevNode.next = n
        originalOrderNodes.append(n)

    # fix first and last node
    originalOrderNodes[0].prev = originalOrderNodes[-1]
    originalOrderNodes[-1].next = originalOrderNodes[0]

    return originalOrderNodes


def moveNode(node: Node):
    if node.value == 0:
        return

    targetNode: Node = node
    steps: int = node.value

    chainLength = len(data) - 1  # -1 because we will remove the current node
    if steps > chainLength:
        steps = steps % chainLength
    if steps < -chainLength:
        steps = -(abs(steps) % chainLength)

    if steps == 0:
        # this can happen if the number is just an integer number of turns
        return

    # print("\t\tnb of steps", steps)

    # Remove node from chain
    assert node.prev
    assert node.next
    node.prev.next = node.next
    node.next.prev = node.prev

    while steps > 0:
        assert targetNode.next is not None
        targetNode = targetNode.next
        steps -= 1
    while steps < 0:
        assert targetNode.prev is not None
        targetNode = targetNode.prev
        steps += 1

    # Place node into chain
    if node.value > 0:
        node.prev = targetNode
        node.next = targetNode.next

        assert targetNode.next is not None
        targetNode.next.prev = node
        targetNode.next = node
    else:
        assert node.value < 0
        node.next = targetNode
        node.prev = targetNode.prev

        assert targetNode.prev is not None
        targetNode.prev.next = node
        targetNode.prev = node


part1Chain = getChainFromData(data)
zeroNode: Node = [n for n in part1Chain if n.value == 0][0]


for node in part1Chain:
    # print("Moving node", node.value)
    moveNode(node)

coordsPart1 = []
coordNode: Node = zeroNode
for idx in range(3000):
    # print("idx", idx)
    assert coordNode.next
    coordNode = coordNode.next

    if (idx + 1) % 1000 == 0:
        coordsPart1.append(coordNode.value)

print(coordsPart1)
print("Part 1", sum(coordsPart1))


# -14734 not the right input (used modulo incorrectly)
# 9194 not the right input (used modulo incorrectly)
# 12491 (too low) because I did not remove the node from the chain before moving it

part2Chain = getChainFromData(data, isPart2=True)
zeroNode: Node = [n for n in part2Chain if n.value == 0][0]


def checkChainIntegrity(chain):
    # print("\tCHECKING INTEGRITY")
    firstNode = chain[0]
    # print("\t", firstNode.value)
    currentNode = firstNode.next
    steps = 1
    while currentNode is not firstNode:
        assert steps < len(chain)

        steps += 1
        currentNode = currentNode.next

    # print("\t", steps, len(chain))
    assert steps == len(chain)


for _ in range(10):
    print("Round", _)
    for node in part2Chain:
        # print("\t", "node", node.value)
        moveNode(node)
        checkChainIntegrity(part2Chain)


coordsPart2 = []
coordNode: Node = zeroNode
for idx in range(3000):
    # print("idx", idx)
    assert coordNode.next
    coordNode = coordNode.next

    if (idx + 1) % 1000 == 0:
        coordsPart2.append(coordNode.value)

print(coordsPart2)
print("Part 2", sum(coordsPart2))


# 8032297847241 too high
# the error was that I was removing node without adding them back
# when the number of steps modulo length was equal to 0
