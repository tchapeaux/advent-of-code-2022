# Don't run this on the input as it will never finish and burn your PC...

from collections import deque
from itertools import product
import math
import re

import aoc

# data = aoc.getLinesForDay(16)
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
usefulValves = set([v for v in valvesDict.keys() if valvesDict[v][0] > 0])

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
    if valvesDict[key][0] == 0 and key != "AA":
        del shortestPathMap[key]
    else:
        for key2 in list(shortestPathMap[key].keys()):
            if valvesDict[key2][0] == 0 and key != "AA":
                del shortestPathMap[key][key2]
            else:
                shortestPathMap[key][key2] = len(shortestPathMap[key][key2])

# print("Simplified Shortest paths dict", (shortestPathMap))


# Vars for Part 2

bestKnownPath = 0
bestValueAtState = dict()

# Exploration algo for Part2


def simulateOneStepWithElephant(
    currentTick,
    humanValveGoal,
    humanTravelRemain,
    elephantValveGoal,
    elephantTravelRemain,
    openedValves,
    accReleasedPresure,
):
    global bestKnownPath
    global alreadySeenCnt
    global doomCnt
    pressureFromOpenedValve = sum(valvesDict[id][0] for id in openedValves)

    # State in "canonical" form (where human and elephant are interchangeable)
    humanState = (humanValveGoal, humanTravelRemain)
    elephantState = (elephantValveGoal, elephantTravelRemain)
    actorsState = sorted([humanState, elephantState])
    state = (
        currentTick,
        tuple(actorsState),
        "-".join(sorted(openedValves)),
    )

    # print(state)

    currentPressure = accReleasedPresure + pressureFromOpenedValve
    if state in bestValueAtState:
        # print("Already seen this state")
        bestValueKnown = bestValueAtState[state]
        if currentPressure > bestValueKnown:
            bestValueAtState[state] = currentPressure
        else:
            alreadySeenCnt += 1
            return
    else:
        bestValueAtState[state] = currentPressure

    # End condition
    if currentTick == 26:
        # print("=", state, "End tick")
        totalPressure = accReleasedPresure + pressureFromOpenedValve
        if totalPressure > bestKnownPath:
            bestKnownPath = totalPressure
            print(
                "Current best path:",
                totalPressure,
                len(bestValueAtState),
                alreadySeenCnt,
                doomCnt,
                "t:",
                aoc.getTick(),
            )
        return

    assert currentTick < 26

    unopenedValves = [v for v in valvesDict.keys() if v not in openedValves]
    usefulUnopenedValves = [v for v in unopenedValves if v in usefulValves]

    # Is there still a chance? => calculate upper bound of potential gains
    # Reasoning: we can still open two valves at each tick, let's simulate best-case scenario
    unopenedValvesPressure = [valvesDict[v][0] for v in usefulUnopenedValves]
    remainingTime = 26 - currentTick
    accPotentialGain = accReleasedPresure + pressureFromOpenedValve * remainingTime
    for idx, pressure in enumerate(sorted(unopenedValvesPressure)[::-1]):
        accPotentialGain += pressure * max(0, remainingTime - math.ceil(idx / 2) - 1)
    if accReleasedPresure + accPotentialGain < bestKnownPath:
        # Doomed to fail
        # print("Doomed to fail")
        doomCnt += 1
        return

    if len(usefulUnopenedValves) == 0:
        # If all useful valves are opened, just wait for the ticks to be over
        # (This is only useful for the examples, as it cannot happen on the real input)
        # print("=", state, "Just waiting now")
        return simulateOneStepWithElephant(
            currentTick + 1,
            humanValveGoal,
            0,
            elephantValveGoal,
            0,
            openedValves,
            accReleasedPresure + pressureFromOpenedValve,
        )

    # Enumerate all options for human + elephant
    # For that, look only at the shortest paths to all unopened valve

    usefulHumanChoices = set()
    if humanTravelRemain == 0:
        if humanValveGoal not in openedValves and humanValveGoal in usefulValves:
            usefulHumanChoices.add("OPEN")
        else:
            # Find another goal
            unopenedValvesByHumanGain = sorted(
                usefulUnopenedValves,
                key=lambda v: valvesDict[v][0]
                * (remainingTime - shortestPathMap[humanValveGoal][v]),
            )
            usefulHumanChoices.update(
                [v for v in unopenedValvesByHumanGain if v != humanValveGoal]
            )
            if len(usefulUnopenedValves) == 1:
                # There could be a conflict there
                # => Add WAIT to the list of possible actions
                usefulHumanChoices.add("WAIT")
    else:
        usefulHumanChoices.add("TRAVEL")

    usefulElephantChoices = set()
    if elephantTravelRemain == 0:
        if elephantValveGoal not in openedValves and elephantValveGoal in usefulValves:
            usefulElephantChoices.add("OPEN")
        else:
            unopenedValvesByElephantGain = sorted(
                usefulUnopenedValves,
                key=lambda v: valvesDict[v][0]
                * (remainingTime - shortestPathMap[elephantValveGoal][v]),
            )
            usefulElephantChoices.update(
                [v for v in unopenedValvesByElephantGain if v != elephantValveGoal]
            )
            if len(usefulUnopenedValves) == 1:
                # There could be a conflict there
                # => Add WAIT to the list of possible actions
                usefulElephantChoices.add("WAIT")
    else:
        usefulElephantChoices.add("TRAVEL")

    # Explore all combination of options
    for humanChoice, elephantChoice in product(
        usefulHumanChoices, usefulElephantChoices
    ):
        # print("=", state, "CHOICES", humanChoice, elephantChoice)

        # If both human and elephant are travelling, skip the intermediate steps
        if humanChoice == elephantChoice == "TRAVEL":
            timeToFirstArrival = min(humanTravelRemain, elephantTravelRemain)
            timeToElapse = min(26 - currentTick, timeToFirstArrival)  # don't overshoot
            return simulateOneStepWithElephant(
                currentTick + timeToElapse,
                humanValveGoal,
                humanTravelRemain - timeToElapse,
                elephantValveGoal,
                elephantTravelRemain - timeToElapse,
                openedValves,
                accReleasedPresure + pressureFromOpenedValve * timeToElapse,
            )

        newHumanValveGoal = humanValveGoal
        newHumanTravelRemain = humanTravelRemain
        newElephantValveGoal = elephantValveGoal
        newElephantTravelRemain = elephantTravelRemain
        newOpenedValves = []
        newOpenedValves.extend(openedValves)

        if (
            humanChoice == elephantChoice == "OPEN"
            and newHumanValveGoal == newElephantValveGoal
        ):
            # Invalid state, skip
            # print("Skip (dual open)")
            continue

        if humanChoice == "OPEN":
            newOpenedValves.append(humanValveGoal)
        elif humanChoice == "TRAVEL":
            newHumanTravelRemain -= 1
        elif humanChoice == "WAIT":
            pass
        else:
            newHumanValveGoal = humanChoice
            newHumanTravelRemain = shortestPathMap[humanValveGoal][newHumanValveGoal]
            # Already travel one step
            newHumanTravelRemain -= 1

        if elephantChoice == "OPEN":
            newOpenedValves.append(elephantValveGoal)
        elif elephantChoice == "TRAVEL":
            newElephantTravelRemain -= 1
        elif elephantChoice == "WAIT":
            pass
        else:
            newElephantValveGoal = elephantChoice
            newElephantTravelRemain = shortestPathMap[elephantValveGoal][
                newElephantValveGoal
            ]
            # Already travel one step
            newElephantTravelRemain -= 1

        # If both human and elephant have the same goal, it won't work => skip
        if newHumanValveGoal == newElephantValveGoal:
            # print("Skip (same goal)")
            continue

        simulateOneStepWithElephant(
            currentTick + 1,
            newHumanValveGoal,
            newHumanTravelRemain,
            newElephantValveGoal,
            newElephantTravelRemain,
            newOpenedValves,
            accReleasedPresure + pressureFromOpenedValve,
        )


# Part 2

simulateOneStepWithElephant(1, "AA", 0, "AA", 0, [], 0)

# Tried: 1320 (too low -- tried the best known value while the logicial was looping forever)
# 1359 (idem)
# 1446
# 1852 (just trying the best answer I find before crash each time I optimize)

print("Visited", len(bestValueAtState), "states")
print("Part 2", bestKnownPath)
print("Found in", aoc.getTick())

# 1943 (???)
# 1944
# 1974
# 2022
