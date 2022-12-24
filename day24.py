from functools import cache
import heapq
from math import lcm
from typing import Set, Tuple

import aoc

data = aoc.getCellsForDay(24)
# data = aoc.getCellsForDay(24, force_filepath="inputs/day24_example.txt")

# Data structure and constants

Position = Tuple[int, int]

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

DIRECTION_MAP = {"^": UP, "v": DOWN, "<": LEFT, ">": RIGHT}

# Coordinate system: (0, 0) is the topleft of the room (walls are in -1)


roomHeight = len(data) - 2
roomWidth = len(data[0]) - 2

blizzardPeriod = lcm(roomHeight, roomWidth)


class Blizzard:
    def __init__(self, initialPos, direction):
        self.initialPos: Position = initialPos
        self.direction = direction

    def getPositionAtTick(self, tick):
        periodicTick = tick % blizzardPeriod
        return (
            (self.initialPos[0] + self.direction[0] * periodicTick) % roomWidth,
            (self.initialPos[1] + self.direction[1] * periodicTick) % roomHeight,
        )


# Parse input

initialPos: Position = (0, -1)  # hardcoded because constant
targetPos: Position = (roomWidth - 1, roomHeight)  # semi-hardcoded because constant

blizzards: Set[Blizzard] = set()
for y, row in enumerate(data[1:-1]):
    for x, cell in enumerate(row[1:-1]):
        if cell in "<>^v":
            blizzards.add(Blizzard((x, y), DIRECTION_MAP[cell]))
        else:
            assert cell == "."


@cache
def getAllBlizzardsPositionsAt(tick) -> Set[Position]:
    bliz = set([b.getPositionAtTick(tick) for b in blizzards])
    return bliz


def getStateScore(position, endPos, tick):
    # The score of a state is used to determine the best path to explore in the greedy exploration
    # We are using a heapq, so the smaller score = the most promising path to explore
    # Basic implementation: the cost is the distance to exit minus the current tick
    distToEnd = aoc.manhattanDistance(position[0], position[1], endPos[0], endPos[1])
    return distToEnd + tick


def findPath(startPos, endPos, initialTick):
    frontier = [(getStateScore(startPos, endPos, initialTick), startPos, initialTick)]
    visited = set()

    while len(frontier) > 0:

        (_, currentPos, currentTick) = heapq.heappop(frontier)

        currentState = (currentPos, currentTick)
        if currentState in visited:
            continue
        visited.add(currentState)

        nextTickBlizzards = getAllBlizzardsPositionsAt(
            (currentTick + 1) % blizzardPeriod
        )
        moves = ((1, 0), (0, 1), (-1, 0), (0, -1), (0, 0))
        for move in moves:
            newPos = (currentPos[0] + move[0], currentPos[1] + move[1])
            if newPos in nextTickBlizzards:
                continue

            if newPos == endPos:
                return currentTick + 1

            if newPos[0] < 0 or newPos[0] >= roomWidth:
                continue
            if newPos[1] < 0 or newPos[1] >= roomHeight:
                continue

            if (newPos, currentTick + 1) in visited:
                continue

            # All checks passed, add to frontier
            heapq.heappush(
                frontier,
                (
                    getStateScore(newPos, endPos, currentTick + 1),
                    newPos,
                    currentTick + 1,
                ),
            )

    print("Could not find path")
    return -1


print("Init:", aoc.getTick())
print("Pre-generating blizzard tables")
for tick in range(blizzardPeriod):
    getAllBlizzardsPositionsAt(tick)
print("Generated in", aoc.getTick())

firstPathLength = findPath(initialPos, targetPos, initialTick=0)
print("Part 1", firstPathLength)
print("Found in", aoc.getTick())

secondPathLength = findPath(targetPos, initialPos, initialTick=firstPathLength)
print("(intermediate)", secondPathLength)
print("Found in ", aoc.getTick())

thirdPathLength = findPath(initialPos, targetPos, initialTick=(secondPathLength))
print("Part 2", thirdPathLength)
print("Found in", aoc.getTick())
