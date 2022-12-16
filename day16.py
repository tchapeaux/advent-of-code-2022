from collections import deque
import re

import aoc

data = aoc.getLinesForDay(16)
data = aoc.getLinesForDay(16, force_filepath="inputs/day16_example.txt")
# data = aoc.getLinesForDay(16, force_filepath="inputs/day16_minimal.txt")

doomCnt = 0
alreadySeenCnt = 0

# Parsing

valvesDict = {}
parseRegex = r"^Valve (\w+) has flow rate=(\d+); tunnels? leads? to valves? (.+)$"
for line in data:
    s = re.search(parseRegex, line.strip())
    assert s is not None
    [valveId, valveFlowRate, valveExits] = s.groups()

    valvesDict[valveId] = [int(valveFlowRate), valveExits.strip().split(", ")]

# print(len(valvesDict.keys()), "valves")


def getPressure(v):
    return valvesDict[v][0]


usefulValves = set([v for v in valvesDict.keys() if getPressure(v) > 0])


# Helper map: give shortest path between all valve pairs

shortestPathMap = {}

for valve1 in valvesDict.keys():
    shortestPathMap[valve1] = {}
    for valve2 in valvesDict.keys():

        # quick implementation of BFS
        frontier = deque([(valve1, [])])
        visited = set([valve1])
        while len(frontier) > 0:
            currentValve, currentPath = frontier.popleft()
            visited.add(currentValve)
            # print(valve1, currentValve, valve2, currentPath)
            if currentValve == valve2:
                shortestPathMap[valve1][valve2] = currentPath
                # print("Found path", valve1, "->", valve2, ":", currentPath)
                break

            nextPaths = valvesDict[currentValve][1]
            for path in nextPaths:
                if path not in visited:
                    frontier.append((path, currentPath + [path]))

# print("Shortest paths dict", (shortestPathMap))

# Simplify shortest paths dict
# Only retain info about useful valves
# Only retain the length between each useful valve
# Also retain the starting point to avoid crashing later on
for key in list(shortestPathMap.keys()):
    if key not in usefulValves and key != "AA":
        del shortestPathMap[key]
    else:
        for key2 in list(shortestPathMap[key].keys()):
            if key2 not in usefulValves or key2 == key:
                del shortestPathMap[key][key2]
            else:
                shortestPathMap[key][key2] = len(shortestPathMap[key][key2])

"""
for key in shortestPathMap:
    print(key)
    for key2 in shortestPathMap[key]:
        print("\t", key2, shortestPathMap[key][key2])
"""


def getTickToFollowPath(path):
    currentValve = "AA"
    accTick = 0
    for valve in path:
        accTick += shortestPathMap[currentValve][valve]
        accTick += 1  # open
        currentValve = valve
    return accTick


def getPressureInPath(path, maxTick):
    currentValve = "AA"
    accPressure = 0
    accTick = 0
    for valve in path:
        distToValve = shortestPathMap[currentValve][valve]
        # print("Move to", valve, "in", distToValve)
        accTick += distToValve
        accTick += 1  # open
        remainingTime = maxTick - accTick
        accPressure += getPressure(valve) * remainingTime
        currentValve = valve
    return accPressure


# Generate all paths


def getPaths(currentPath, maxTick):
    # print("exploring", currentPath, getTickToFollowPath(currentPath))
    currentTick = getTickToFollowPath(currentPath)
    if currentTick == maxTick:
        yield currentPath
    elif currentTick > maxTick:
        yield currentPath[:-1]
    else:
        lastValve = currentPath[-1] if len(currentPath) > 0 else "AA"
        nextValves = [
            v for v in shortestPathMap[lastValve].keys() if v not in currentPath
        ]
        for nValve in nextValves:
            for nPath in getPaths(currentPath + [nValve], maxTick):
                yield nPath
        if len(nextValves) == 0:
            yield currentPath


paths = set()
for path in getPaths([], maxTick=30):
    paths.add(tuple(path))

print("Found", len(paths), "paths")

sortedPaths = sorted(
    [p for p in paths], key=lambda p: getPressureInPath(p, maxTick=30), reverse=True
)

bestPath = sortedPaths[0]
print("Part 1", getPressureInPath(bestPath, maxTick=30))

# Part 2

paths = set()
for path in getPaths([], maxTick=26):
    paths.add(tuple(path))


print("Found", len(paths), "paths")

sortedPaths = sorted(
    [p for p in paths], key=lambda p: getPressureInPath(p, maxTick=26), reverse=True
)

# Explore paths until you find another path that is completely separated from bestPath
for path in sortedPaths[1:]:
    if all([valve not in bestPath for valve in path]):
        print(
            "Part 2",
            getPressureInPath(bestPath, maxTick=26)
            + getPressureInPath(path, maxTick=26),
        )
        print(bestPath)
        print(path)
        break
