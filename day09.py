import aoc

data = aoc.getLinesForDay(9)
# data = aoc.getLinesForDay(9, force_filepath="inputs/day09_fun_from_web.txt")

DIR_ENUMS = {"U": (0, -1), "D": (0, 1), "L": (-1, 0), "R": (1, 0)}


# Parse
instructions = []
for line in data:
    [direction, length] = line.split(" ")
    instructions.append((direction, int(length)))

# Keep-up logic
def keepUp(headPos, tailPos):
    """
    Return the new pos of a node based on the previous node
    @param headPos position of the previous node at step N
    @param tailPos position of the current node at step N-1
    @returns position of the current node at step N
    """
    dX = headPos[0] - tailPos[0]
    dY = headPos[1] - tailPos[1]

    newPos = [tailPos[0], tailPos[1]]

    if -1 <= dX <= 1 and -1 <= dY <= 1:
        return newPos

    # Vertical case
    if dX == 0:
        assert abs(dY) == 2
        newPos[1] += dY / 2
        return newPos

    # Horizontal case
    if dY == 0:
        assert abs(dX) == 2
        newPos[0] += dX / 2
        return newPos

    # Diagonal case
    # we want to move the tail in the direction of
    # (dX, dY) but normalized to length 1 in each direction
    assert dX != 0 and dY != 0
    normDX = dX / abs(dX)
    normDY = dY / abs(dY)
    newPos[0] += normDX
    newPos[1] += normDY
    return newPos


def getVisualization(visited):
    minX = min(int(x[0]) for x in visited)
    maxX = max(int(x[0]) for x in visited)
    minY = min(int(x[1]) for x in visited)
    maxY = max(int(x[1]) for x in visited)

    rows = []
    for y in range(minY, maxY + 1):
        row = ""
        for x in range(minX, maxX + 1):
            row += "€" if (x, y) in visited else " "
        rows.append(row)
    return "\n".join(rows)


# Simulate Part 1

headPos = [0, 0]
tailPos = [0, 0]
visitedPart1 = set()

for [_dir, _len] in instructions:
    dirVector = DIR_ENUMS[_dir]

    for step in range(_len):
        headPos[0] += dirVector[0]
        headPos[1] += dirVector[1]

        tailPos = keepUp(headPos, tailPos)

        visitedPart1.add((tailPos[0], tailPos[1]))

print("Part 1", len(visitedPart1))
# print(getVisualization(visitedPart1))


# Simulate Part 2 (10 nodes)
nodesPos = [[0, 0] for _ in range(10)]
visitedPart2 = set()

for instrIdx, [_dir, _len] in enumerate(instructions):
    dirVector = DIR_ENUMS[_dir]

    for step in range(_len):
        # print(_dir, _len, "step", step)
        # Move head
        nodesPos[0][0] += dirVector[0]
        nodesPos[0][1] += dirVector[1]

        # Simulate each subsequent node
        for nodeIdx in range(1, len(nodesPos)):
            newPos = keepUp(nodesPos[nodeIdx - 1], nodesPos[nodeIdx])
            # print("new", newPos)
            nodesPos[nodeIdx] = newPos

        # Store tail position
        tailNodePos = nodesPos[-1]
        # print("tail", nodesPos, tailNodePos)
        visitedPart2.add((tailNodePos[0], tailNodePos[1]))
print("Part 2", len(visitedPart2))
# print(getVisualization(visitedPart2))
