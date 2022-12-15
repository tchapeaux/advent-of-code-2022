import re

import aoc

data = aoc.getLinesForDay(15)
# data = aoc.getLinesForDay(15, force_filepath="inputs/day15_example.txt")
# data = aoc.getLinesForDay(15, force_filepath="inputs/day15_minimal.txt")

sensorBeaconDict = {}

for line in data:
    findNumbersRegex = r"(-?\d+)"
    sX, sY, bX, bY = re.findall(findNumbersRegex, line)
    sensorPos = (int(sX), int(sY))
    beaconPos = (int(bX), int(bY))

    sensorBeaconDict[sensorPos] = beaconPos

# print(sensorBeaconDict)


def countNonBeaconableAtRow(rowIdx):
    nonBeaconableX = set()

    for [(sX, sY), (bX, bY)] in sensorBeaconDict.items():
        distToClosestBeacon = aoc.manhattanDistance(sX, sY, bX, bY)
        distY = abs(rowIdx - sY)
        remainingDistX = distToClosestBeacon - distY

        if remainingDistX >= 0:
            for xx in range(sX - remainingDistX, sX + remainingDistX + 1):
                if (xx, rowIdx) not in sensorBeaconDict.values():
                    nonBeaconableX.add((xx, rowIdx))

    # print(sorted(list(nonBeaconableX)))

    return len(nonBeaconableX)


part1 = countNonBeaconableAtRow(2000000)
assert part1 < 5100464  # first wrong guess
print("Part 1", countNonBeaconableAtRow(2000000))
# Found the first star by realizing my algorithm was wrong by one on the example
# and trying to submit my wrong output - 1 🙈
# => My error was counting the beacons itself, which are easily removed


def findNonBeaconableCell(rowIdx):
    # Found the algorithm general idea from Reddit and adapted it a bit
    nonBeaconableSegments = set()

    # Create segments
    for [(sX, sY), (bX, bY)] in sensorBeaconDict.items():
        distToClosestBeacon = aoc.manhattanDistance(sX, sY, bX, bY)
        distY = abs(rowIdx - sY)
        remainingDistX = distToClosestBeacon - distY

        if remainingDistX >= 0:
            nonBeaconableSegments.add((sX - remainingDistX, sX + remainingDistX))

    # Find gap in segment
    segments = sorted(nonBeaconableSegments)
    assert segments[0][0] <= 0
    currentMax = segments[0][1]
    for s in segments:
        if s[0] > currentMax:
            # FOUND THE GAP
            # We know there is only one cell, so we return the X coordinate
            return currentMax + 1
        currentMax = max(currentMax, s[1])

    assert currentMax >= 4000000

    return False


for row in range(4000000):
    """
    if row % 1000 == 0:
        print(row)
    """

    gapXIfAny = findNonBeaconableCell(row)
    if gapXIfAny:
        print("Part 2", gapXIfAny * 4000000 + row)
        break

print(aoc.getTick())
