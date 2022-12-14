import aoc


# Parse input

data = aoc.getLinesForDay(14)
# data = aoc.getLinesForDay(14, force_filepath="inputs/day14_example.txt")


def readRocks(data):
    rockBlocks = set()
    for line in data:
        points = line.split(" -> ")
        points = [(int(p.split(",")[0]), int(p.split(",")[1])) for p in points]

        # Trace path
        currentPoint = points[0]
        for p in points[1:]:
            rockBlocks.add(points[0])
            assert (p[1] == currentPoint[1]) ^ (p[0] == currentPoint[0])
            if p[1] == currentPoint[1]:
                xDirection = int((p[0] - currentPoint[0]) / abs(p[0] - currentPoint[0]))
                for dx in range(p[0], currentPoint[0], -xDirection):
                    rockBlocks.add((dx, p[1]))
            elif p[0] == currentPoint[0]:
                yDirection = int((p[1] - currentPoint[1]) / abs(p[1] - currentPoint[1]))
                for dy in range(p[1], currentPoint[1], -yDirection):
                    rockBlocks.add((p[0], dy))
            currentPoint = p
    return rockBlocks


# Helper functions


def getVisualGrid(rockBlocks, sandBlocks):
    minX = min([r[0] for r in rockBlocks])
    maxX = max([r[0] for r in rockBlocks])
    minY = min([r[1] for r in rockBlocks])
    maxY = max([r[1] for r in rockBlocks])

    rows = [f"${minX} {maxX} {minY} {maxY}"]
    for y in range(min(0, minY), maxY + 1):
        rowStr = ""
        for x in range(minX, maxX):
            if x == 500 and y == 0:
                rowStr += "+"
            elif (x, y) in rockBlocks:
                rowStr += "#"
            elif (x, y) in sandBlocks:
                rowStr += "."
            else:
                rowStr += " "
        rows.append(rowStr)

    return "\n".join(rows)


def simulateOneSandBlock(rockBlocks, sandBlocks, hasFloor=False):
    """
    Full simulation of one new sand block
    - Place the new block in sandBlocks
    - Return True if at rest, False if infinite fall
    """
    sandX = 500
    sandY = 0
    lowestRockY = max([r[1] for r in rockBlocks])

    while True:
        if hasFloor:
            # Part 2 logic: rest on the infinite floor
            if sandY == lowestRockY + 1:
                break
        else:
            # Part 1 logic: infinite fall to bottom
            if sandY > lowestRockY:
                return False

        newPos = (sandX, sandY + 1)
        if newPos not in rockBlocks and newPos not in sandBlocks:
            sandX, sandY = newPos
            continue

        newPos = (sandX - 1, sandY + 1)
        if newPos not in rockBlocks and newPos not in sandBlocks:
            sandX, sandY = newPos
            continue

        newPos = (sandX + 1, sandY + 1)
        if newPos not in rockBlocks and newPos not in sandBlocks:
            sandX, sandY = newPos
            continue

        # If we reach this point, the new sand block is at rest
        break

    sandBlocks.add((sandX, sandY))
    return True


# Launch simulation


rockBlocks = readRocks(data)

# Part 1
sandBlocks = set()
# print(getVisualGrid(rockBlocks, sandBlocks))
sandBlockCounter = 0
while True:
    isAtRest = simulateOneSandBlock(rockBlocks, sandBlocks, hasFloor=False)
    if isAtRest:
        sandBlockCounter += 1
    else:
        break

print(getVisualGrid(rockBlocks, sandBlocks))
print("Part 1", sandBlockCounter)

# Part 2
sandBlocks = set()
sandBlockCounter = 0
sandBlockCounter = 0
while True:
    isAtRest = simulateOneSandBlock(rockBlocks, sandBlocks, hasFloor=True)
    assert isAtRest
    sandBlockCounter += 1

    if (500, 0) in sandBlocks:
        # Sand source is blocked
        break

print(getVisualGrid(rockBlocks, sandBlocks))
print("Part 2", sandBlockCounter)
print("Found in ", aoc.getTick())
