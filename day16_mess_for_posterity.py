# Don't run this on the input as it will never finish and burn your PC...

from collections import deque
from itertools import product
import math
import re

import aoc

# data = aoc.getLinesForDay(16)
data = aoc.getLinesForDay(16, force_filepath="inputs/day16_example.txt")
# data = aoc.getLinesForDay(16, force_filepath="inputs/day16_minimal.txt")


# Parsing

valvesDict = {}
parseRegex = r"^Valve (\w+) has flow rate=(\d+); tunnels? leads? to valves? (.+)$"
for line in data:
    s = re.search(parseRegex, line.strip())
    assert s is not None
    [valveId, valveFlowRate, valveExits] = s.groups()

    valvesDict[valveId] = [int(valveFlowRate), valveExits.strip().split(", ")]

print(len(valvesDict.keys()), "valves")

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
        else:
            print("Could not find path")

# print("Shortest paths dict", (shortestPathMap))


# Exploration algo for Part 1

bestKnownPath = 0

knownStates = set()


def simulateOneStep(currentTick, currentValve, openedValves, accReleasedPresure):
    global bestKnownPath
    pressureFromOpenedValve = sum(valvesDict[id][0] for id in openedValves)

    # print("STEP", currentTick, currentValve, openedValves, accReleasedPresure)
    state = (currentTick, currentValve, "".join(openedValves), accReleasedPresure)
    if state in knownStates:
        # print("Already seen this state")
        return
    else:
        knownStates.add(state)

    # End condition
    if currentTick == 30:
        totalPressure = accReleasedPresure + pressureFromOpenedValve
        if totalPressure > bestKnownPath:
            bestKnownPath = totalPressure
            print("Current best path:", totalPressure)
        return

    # Is there still a chance? => calculate upper bound of potential gains
    # Reasoning: we can still open one valve at each tick, let's simulate best-case scenario
    unopenedValvesPressure = [
        valvesDict[v][0] for v in valvesDict.keys() if v not in openedValves
    ]
    remainingTime = 30 - currentTick
    accPotentialGain = accReleasedPresure + pressureFromOpenedValve * remainingTime
    for idx, pressure in enumerate(sorted(unopenedValvesPressure)[::-1]):
        accPotentialGain += pressure * (remainingTime - idx - 1)
    if accReleasedPresure + accPotentialGain < bestKnownPath:
        # Doomed to fail
        # print("Doomed to fail")
        return

    if len(openedValves) == len(valvesDict):
        # If all valves are opened, just wait for the ticks to be over
        # (This is only useful for the examples, as it cannot happen on the real input)
        return simulateOneStep(
            currentTick + 1,
            currentValve,
            openedValves,
            accReleasedPresure + pressureFromOpenedValve,
        )

    if currentValve not in openedValves and valvesDict[currentValve][0] > 0:
        # Explore opening the valve
        newOpenedValves = []
        newOpenedValves.extend(openedValves)
        newOpenedValves.append(currentValve)
        simulateOneStep(
            currentTick + 1,
            currentValve,
            newOpenedValves,
            accReleasedPresure + pressureFromOpenedValve,
        )

    # Explore going down the exits
    for exit in valvesDict[currentValve][1]:
        simulateOneStep(
            currentTick + 1,
            exit,
            openedValves,
            accReleasedPresure + pressureFromOpenedValve,
        )

    # Another option: doing nothing
    # => Not explored because it's never useful


# Part 1

simulateOneStep(1, "AA", [], 0)

# Wrong answers:
# 239 (too low) because my algo was stuck on this value os I thought let's try it
# 342 (same thing)

print("Visited", len(knownStates), "states")
print("Part 1", bestKnownPath)
print("Found in", aoc.getTick())

# Reset for Part 2

bestKnownPath = 0
knownStates = set()

# Exploration algo for Part2


def simulateOneStepWithElephant(
    currentTick, humanValve, elephantValve, openedValves, accReleasedPresure
):
    global bestKnownPath
    pressureFromOpenedValve = sum(valvesDict[id][0] for id in openedValves)

    state = (
        currentTick,
        accReleasedPresure,
        humanValve,
        elephantValve,
        "-".join(sorted(openedValves)),
    )
    # human and elephant are interchangeable
    reversedState = (
        currentTick,
        accReleasedPresure,
        elephantValve,
        humanValve,
        "-".join(sorted(openedValves)),
    )
    # print(state)
    if state in knownStates or reversedState in knownStates:
        # print("Already seen this state")
        return
    else:
        knownStates.add(state)

    # End condition
    if currentTick == 26:
        totalPressure = accReleasedPresure + pressureFromOpenedValve
        if totalPressure > bestKnownPath:
            bestKnownPath = totalPressure
            print("Current best path:", totalPressure, len(knownStates))
        return

    unopenedValves = [v for v in valvesDict.keys() if v not in openedValves]

    # Is there still a chance? => calculate upper bound of potential gains
    # Reasoning: we can still open two valves at each tick, let's simulate best-case scenario
    unopenedValvesPressure = [valvesDict[v][0] for v in unopenedValves]
    remainingTime = 26 - currentTick
    accPotentialGain = accReleasedPresure + pressureFromOpenedValve * remainingTime
    for idx, pressure in enumerate(sorted(unopenedValvesPressure)[::-1]):
        accPotentialGain += pressure * max(0, remainingTime - math.ceil(idx / 2) - 1)
    if accReleasedPresure + accPotentialGain < bestKnownPath:
        # Doomed to fail
        # print("Doomed to fail")
        return

    if len(openedValves) == len(valvesDict):
        # If all valves are opened, just wait for the ticks to be over
        # (This is only useful for the examples, as it cannot happen on the real input)
        return simulateOneStepWithElephant(
            currentTick + 1,
            humanValve,
            elephantValve,
            openedValves,
            accReleasedPresure + pressureFromOpenedValve,
        )

    # Enumerate all options for human + elephant
    # For that, look only at the shortest paths to all unopened valve

    unopenedValvesByHumanGain = sorted(
        unopenedValves,
        key=lambda v: valvesDict[v][0]
        * (remainingTime - len(shortestPathMap[humanValve][v])),
    )
    usefulHumanChoices = set(
        [
            shortestPathMap[humanValve][v][0]
            for v in unopenedValvesByHumanGain
            if len(shortestPathMap[humanValve][v]) > 0
        ]
    )
    unopenedValvesByElephantGain = sorted(
        unopenedValves,
        key=lambda v: valvesDict[v][0]
        * (remainingTime - len(shortestPathMap[elephantValve][v])),
    )
    usefulElephantChoices = set(
        [
            shortestPathMap[elephantValve][v][0]
            for v in unopenedValvesByElephantGain
            if len(shortestPathMap[elephantValve][v]) > 0
        ]
    )

    humanOptions = []
    if humanValve not in openedValves and valvesDict[humanValve][0] > 0:
        humanOptions.append("OPEN")
    humanOptions.extend(list(usefulHumanChoices))
    elephantOptions = []
    if elephantValve not in openedValves and valvesDict[elephantValve][0] > 0:
        elephantOptions.append("OPEN")
    elephantOptions.extend(list(usefulElephantChoices))

    # Explore all combination of options
    for humanChoice, elephantChoice in product(humanOptions, elephantOptions):
        newHumanValve = humanValve
        newElephantValve = elephantValve
        newOpenedValves = []
        newOpenedValves.extend(openedValves)

        if humanChoice == elephantChoice == "OPEN" and humanValve == elephantValve:
            continue

        if humanChoice == "OPEN":
            newOpenedValves.append(humanValve)
        else:
            newHumanValve = humanChoice

        if elephantChoice == "OPEN":
            newOpenedValves.append(elephantValve)
        else:
            newElephantValve = elephantChoice

        simulateOneStepWithElephant(
            currentTick + 1,
            newHumanValve,
            newElephantValve,
            newOpenedValves,
            accReleasedPresure + pressureFromOpenedValve,
        )


# Part 2

simulateOneStepWithElephant(1, "AA", "AA", [], 0)

# Tried: 1320 (too low -- tried the best known value while the logicial was looping forever)
# 1359 (idem)
# 1446
# 1852 (just trying the best answer I find before crash each time I optimize)

print("Visited", len(knownStates), "states")
print("Part 2", bestKnownPath)
print("Found in", aoc.getTick())

# 1943 (???)
