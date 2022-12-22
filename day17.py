from copy import deepcopy
import math

import aoc

data = aoc.getInputForDay(17).strip()
# data = aoc.getInputForDay(17, force_filepath="inputs/day17_example.txt").strip()

ONE_TRILLION = 1000000000000

winds = [c for c in data if c in "<>"]

# define the shapes relative coordinartes
# (0, 0) is the bottom-left corner (will be useful later)
# and Y goes up against all conventions
SHAPE_MINUS = ((0, 0), (1, 0), (2, 0), (3, 0))
SHAPE_PLUS = ((1, 2), (0, 1), (1, 1), (2, 1), (1, 0))
SHAPE_J = ((2, 2), (2, 1), (0, 0), (1, 0), (2, 0))
SHAPE_I = ((0, 3), (0, 2), (0, 1), (0, 0))
SHAPE_SQUARE = ((0, 0), (0, 1), (1, 0), (1, 1))

SHAPES = (SHAPE_MINUS, SHAPE_PLUS, SHAPE_J, SHAPE_I, SHAPE_SQUARE)

# Store the current grid as a hollow matrix
# Only the positions of the filled rocks are stored

grid = []
for _ in range(7):
    grid.append(set([0]))


def pruneGrid(grid):
    # Optimization (?)
    # For each column, find the highest rock
    # Fpr those rocks, find the lowest Y
    # Remove all rocks below it
    highestRocksPerColumn = [max(grid[x]) for x in range(len(grid))]
    lowestHighest = min(highestRocksPerColumn)
    for x in range(len(grid)):
        grid[x] = set([y - lowestHighest for y in grid[x] if y - lowestHighest >= 0])
    return lowestHighest


def doesCollide(rockShape, grid):
    for (x, y) in rockShape:
        if x < 0 or x >= len(grid):
            return True
        if y < 0:
            return True
        if y in grid[x]:
            return True
    return False


def heightOfGrid(grid):
    return max([max(grid[x]) for x in range(len(grid))])


def makeOneRockFall(grid, newRock, windIndex):
    highestRockY = heightOfGrid(grid)
    currentRockBottomLeft = (2, highestRockY + 4)

    currentRock = [
        (currentRockBottomLeft[0] + dx, currentRockBottomLeft[1] + dy)
        for (dx, dy) in newRock
    ]

    currentTick = 0
    while not any([y in grid[x] for (x, y) in currentRock]):

        # Wind
        currentWind = winds[(windIndex + currentTick) % len(winds)]
        # print("Tick", currentTick, "rock", currentRock, "wind", currentWind)
        assert currentWind in "<>"
        newRock = [(x + (1 if currentWind == ">" else -1), y) for (x, y) in currentRock]
        if not doesCollide(newRock, grid):
            currentRock = newRock

        # Gravity
        newRock = [(x, y - 1) for (x, y) in currentRock]
        if doesCollide(newRock, grid):
            # print("\tSettle at", currentRock)
            for (x, y) in currentRock:
                grid[x].add(y)
        else:
            currentRock = newRock

        currentTick += 1

    return windIndex + currentTick


def getGridStr(grid, prunedHeight):
    minY = min([min(grid[x]) for x in range(len(grid))])
    maxY = max([max(grid[x]) for x in range(len(grid))])

    accStr = "pruned: " + str(prunedHeight)
    for y in range(maxY, minY - 1, -1):
        accStr += "\n"
        for x in range(len(grid)):
            accStr += "X" if y in grid[x] else " "

    return accStr


def getHeightOfSimulatedSteps(
    grid, nbOfRocks=2022, initialTick=0, initialPrunedHeight=0
):
    newGrid = deepcopy(grid)
    prunedHeight = initialPrunedHeight

    tick = initialTick
    for rockIdx in range(nbOfRocks):
        prunedHeight += pruneGrid(newGrid)

        # print("Create rock", rockIdx, "at", tick)
        newRock = SHAPES[rockIdx % len(SHAPES)]

        # print(getGridStr(newGrid, prunedHeight))

        tick = makeOneRockFall(newGrid, newRock, tick)

    return prunedHeight + heightOfGrid(newGrid)


print("Part 1")
height = getHeightOfSimulatedSteps(grid, 2022)
print(height)
print("Found in", aoc.getTick())

# 3109 too low

# Part 2


def findPeriodicity():
    newGrid = deepcopy(grid)

    prunedHeight = 0
    knownStates = []
    heightHistory = []
    tick = 0
    rockIdx = 0
    currentState = None
    while True:
        prunedHeight += pruneGrid(newGrid)

        # print("Create rock", rockIdx, "at", tick)
        newRock = SHAPES[rockIdx % len(SHAPES)]

        tick = makeOneRockFall(newGrid, newRock, tick)
        rockIdx += 1
        heightHistory.append(prunedHeight + heightOfGrid(newGrid))

        # print(getGridStr(newGrid, prunedHeight))

        # Store a "canonical state" to find periodicity
        canonicalGrid = {x: tuple(sorted(newGrid[x])) for x in range(len(newGrid))}
        currentState = (
            tick % len(winds),
            rockIdx % len(SHAPES),
            tuple(values for col, values in sorted(canonicalGrid.items())),
        )
        if currentState in knownStates:
            break
        # print(state[0], state[1])

        knownStates.append(currentState)

    firstRepeatingRockIdx = rockIdx
    lastStateRockIdx = knownStates.index(currentState)
    periodLength = firstRepeatingRockIdx - lastStateRockIdx - 1

    deltaHeightHistory = [
        heightHistory[idx] if idx == 0 else heightHistory[idx] - heightHistory[idx - 1]
        for idx in range(len(heightHistory))
    ]

    preambleDeltaHeights = deltaHeightHistory[:-periodLength]
    repeatingDeltaHeights = deltaHeightHistory[-periodLength:]

    return (preambleDeltaHeights, repeatingDeltaHeights)


print("Part 2")

ONE_TRILLION = 1000000000000
# General idea: there is periodicity in the data
# which means that we don't need to simulate every rock

# Find periodicity (repeating state) in the simulation
[preamble, repeating] = findPeriodicity()


# Use math to compute the state after X repeating periods

period = len(repeating)
preambleHeight = sum(preamble)
periodDeltaHeight = sum(repeating)
nbOfPeriods = math.floor((ONE_TRILLION - len(preamble)) / period)
remainingRockNumbers = ONE_TRILLION - (nbOfPeriods * period) - len(preamble)


print(
    "Part 2",
    preambleHeight
    + periodDeltaHeight * (nbOfPeriods)
    + sum(repeating[:remainingRockNumbers]),
)

# 1570930232570 (too low)
# 1570930232573 (too low)

print("Found in", aoc.getTick())
