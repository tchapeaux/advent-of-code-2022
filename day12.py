import heapq
import time
from typing import List, Optional

import aoc

startTick = time.time()

Coords = tuple[int, int]

grid: List[List[str]] = aoc.getCellsForDay(12)


HEIGHT: int = len(grid)
WIDTH: int = len(grid[0])

# Explore input to find S and E

sX, sY = None, None
eX, eY = None, None

for y in range(HEIGHT):
    for x in range(WIDTH):
        if grid[y][x] == "S":
            print(f"✅ Found S: ({x}, {y})")
            sX, sY = x, y
        if grid[y][x] == "E":
            eX, eY = x, y
            print(f"✅ Found E: ({x}, {y})")

assert sX is not None and sY is not None
assert eX is not None and eY is not None

# Helper functions for the path-finding


def getHeight(cellValue: str) -> int:
    if cellValue == "S":
        return ord("a")
    if cellValue == "E":
        return ord("z")
    return ord(cellValue)


def getPathLength(start, goal, knownMax=None):
    # A* implementation based on
    # https://www.redblobgames.com/pathfinding/a-star/introduction.html
    frontier: List[tuple[int, Coords]] = [(0, start)]
    cameFrom: dict[Coords, Optional[Coords]] = {start: None}
    costSoFar: dict[Coords, int] = {start: 0}

    while len(frontier) > 0:
        current = heapq.heappop(frontier)
        x, y = current[1]

        if (x, y) == goal:
            break

        for nextX, nextY, _ in aoc.get4Neighbors(grid, x, y):
            currentHeight = getHeight(grid[y][x])
            nextHeight = getHeight(grid[nextY][nextX])
            if nextHeight - currentHeight > 1:
                continue

            # Each step has a cost of 1
            newCost = costSoFar[(x, y)] + 1
            if knownMax and newCost > knownMax:
                continue

            if (nextX, nextY) not in costSoFar or newCost < costSoFar[(nextX, nextY)]:
                costSoFar[(nextX, nextY)] = newCost
                priority = newCost + aoc.manhattanDistance(nextX, nextY, eX, eY)
                heapq.heappush(frontier, (priority, (nextX, nextY)))
                cameFrom[(nextX, nextY)] = (x, y)

    # Return length if path found, otherwise a big value
    return costSoFar[goal] if goal in costSoFar else 9999999


# Part 1 - Find the path from start

start = (sX, sY)
goal = (eX, eY)
part1Length = getPathLength(start, goal)
print("Part 1", part1Length)
print("Found in ", aoc.getTick())

# Part 2 - Explore all starting point and find closest to end point
startingPoints = set()
for y in range(HEIGHT):
    for x in range(WIDTH):
        if grid[y][x] == "a":
            startingPoints.add((x, y))
currentBestLength = part1Length
currentBestStart = start

for (_x, _y) in startingPoints:
    thisPathLength = getPathLength((_x, _y), goal, knownMax=currentBestLength)
    if thisPathLength < currentBestLength:
        print("\tFound better", _x, _y, "of length", thisPathLength)
        print("\tFound in ", aoc.getTick())
        currentBestLength = thisPathLength
        currentBestStart = (_x, _y)

print("Part 2", currentBestLength)
print("\tFound in ", aoc.getTick())
