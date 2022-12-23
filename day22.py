import re

import aoc

data = aoc.getInputForDay(22)
# data = aoc.getInputForDay(22, force_filepath="inputs/day22_example.txt")

lines = data.split("\n")
grid = []
for line in lines[:-3]:
    grid.append([c for c in line.replace("\n", "")])

instructionsLine = lines[-2]

instructions = []
while len(instructionsLine) > 0:
    match = None
    if instructionsLine[0].isdigit():
        m = re.match(r"^(\d*)", instructionsLine)
        assert m is not None
        match = m.groups()[0]
        instructions.append(int(match))
    else:
        match = instructionsLine[0]
        instructions.append(match)
    instructionsLine = instructionsLine[len(match) :]

initialX = min([idx for idx, value in enumerate(grid[0]) if value == "."])
initialPosition = (initialX, 0, (1, 0))


def getNextPosition(grid, x, y, direction):
    _x = x
    _y = y
    while True:
        _x += direction[0]
        _y += direction[1]

        _y %= len(grid)
        _x %= max([len(grid[__y]) for __y in range(len(grid))])

        if _x >= len(grid[_y]):
            continue
        if grid[_y][_x] == "." or grid[_y][_x] == "#":
            return (_x, _y)
        assert _x != x or _y != y


TURN_RIGHT = {(1, 0): (0, 1), (0, 1): (-1, 0), (-1, 0): (0, -1), (0, -1): (1, 0)}

TURN_LEFT = {(1, 0): (0, -1), (0, -1): (-1, 0), (-1, 0): (0, 1), (0, 1): (1, 0)}

FACING_SCORE = {(1, 0): 0, (0, 1): 1, (-1, 0): 2, (0, -1): 3}

FACING_REPR = {(1, 0): ">", (0, 1): "V", (-1, 0): "<", (0, -1): "^"}

visitedCells = {}
visitCount = {}


def followInstructions(initialPosition, grid, instructions):
    pos = initialPosition
    for ins in instructions:
        print("Current pos", (pos[0] + 1, pos[1] + 1, FACING_SCORE[pos[2]]))
        print("ins", ins)
        if type(ins) == int:
            for step in range(ins):
                nextX, nextY = getNextPosition(grid, pos[0], pos[1], pos[2])
                if grid[nextY][nextX] == ".":
                    pos = (nextX, nextY, pos[2])
                    visitedCells[(pos[1], pos[0])] = FACING_REPR[pos[2]]
                    visitCount[(pos[1], pos[0])] = (
                        1
                        if (pos[1], pos[0]) not in visitCount
                        else visitCount[((pos[1], pos[0]))] + 1
                    )
                else:
                    break
        else:
            assert ins in "LR"
            if ins == "L":
                pos = (pos[0], pos[1], TURN_LEFT[pos[2]])
            else:
                pos = (pos[0], pos[1], TURN_RIGHT[pos[2]])
            visitedCells[(pos[1], pos[0])] = FACING_REPR[pos[2]]
            visitCount[(pos[1], pos[0])] = (
                1
                if (pos[1], pos[0]) not in visitCount
                else visitCount[((pos[1], pos[0]))] + 1
            )

    return pos


finalPos = followInstructions(initialPosition, grid, instructions)

for y, line in enumerate(grid):
    rowStr = ""
    for x, cell in enumerate(line):
        if (y, x) in visitedCells:
            rowStr += visitedCells[(y, x)]
        else:
            rowStr += cell
    # print(rowStr)


print(finalPos)
finalRow = finalPos[1] + 1
finalColumn = finalPos[0] + 1
print(1000 * finalRow + 4 * finalColumn + FACING_SCORE[finalPos[2]])


# 185118 too high
