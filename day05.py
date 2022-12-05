from collections import deque
from copy import deepcopy

import aoc

data = aoc.getInputForDay(5)

# First we parse the data

[gridStr, instructions_str] = data.split("\n\n")
instructions_str = instructions_str.strip().split("\n")

# Parse the grid first

nbOfStacks = int(gridStr[-2])

stacks = [deque() for _ in range(nbOfStacks)]
gridAsMatrix = []

for line in gridStr.split("\n")[:-1]:
    gridAsMatrix.append([])
    for cellIdx in range(nbOfStacks):
        cellVal = line[4 * cellIdx + 1]
        gridAsMatrix[-1].append(cellVal)

# Transpose the matrix into the deque to get the grid into a list of deque

for row in gridAsMatrix[::-1]:
    for stackIdx, cell in enumerate(row):
        if cell != " ":
            stacks[stackIdx].append(cell)

# Parse the instructions


def extractNumbersOnly(sourceStr):
    # Found this bit of code at https://www.geeksforgeeks.org/python-extract-numbers-from-string/
    return [int(x) for x in sourceStr.split(" ") if x.isdigit()]


instructions = []
for instr in instructions_str:
    values = extractNumbersOnly(instr)
    assert len(values) == 3
    assert 1 <= values[1] <= nbOfStacks
    assert 1 <= values[2] <= nbOfStacks
    instructions.append([int(x) for x in values])

# Perform the instructions on the grid (Part 1)

newStacks = deepcopy(stacks)

for [quantity, fromStackIdx, toStackIdx] in instructions:
    for _ in range(quantity):
        value = newStacks[fromStackIdx - 1].pop()
        newStacks[toStackIdx - 1].append(value)

# Get the canopy (complex word just to say the last element of each deque)

print("Part 1", "".join([s[-1] for s in newStacks]))

# Perform the instructions on the grid (Part 2)
# This time, for instructions with quantity > 1, crates are moved in the same order

newStacks2 = deepcopy(stacks)

for [quantity, fromStackIdx, toStackIdx] in instructions:
    buffer = deque()
    for _ in range(quantity):
        value = newStacks2[fromStackIdx - 1].pop()
        buffer.append(value)

    for _ in range(quantity):
        value = buffer.pop()
        newStacks2[toStackIdx - 1].append(value)

print("Part 2", "".join([s[-1] for s in newStacks2]))
