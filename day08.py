import aoc

data = aoc.getNumberCellsForDay(8)
# data = aoc.getNumberCellsForDay(8, force_filepath="inputs/day08_example.txt")
# data = aoc.getNumberCellsForDay(8, force_filepath="inputs/day08_minimal.txt")

# Strategy: Iterate over each row and column in both directions and count

height = len(data)
width = len(data[0])

print("HEIGHT", height)
print("WIDTH", width)

visibleTrees = set()

# Iterate over rows
for y in range(height):
    max_left = -1
    max_right = -1
    for x in range(width):
        if data[y][x] > max_left:
            visibleTrees.add((x, y))
            max_left = data[y][x]
        if data[y][width - 1 - x] > max_right:
            visibleTrees.add((width - 1 - x, y))
            max_right = data[y][width - 1 - x]

# Iterate over columns
for x in range(width):
    max_top = -1
    max_bottom = -1
    for y in range(height):
        if data[y][x] > max_top:
            visibleTrees.add((x, y))
            max_top = data[y][x]
        if data[height - 1 - y][x] > max_bottom:
            visibleTrees.add((x, height - 1 - y))
            max_bottom = data[height - 1 - y][x]


# Print grid of visible tree (for debug)
for yy in range(height):
    rowStr = ""
    for xx in range(width):
        rowStr += "X" if (xx, yy) in visibleTrees else " "
    print(rowStr)

# 3271 too high (was storing the bottom and left visible trees incorrectly)

print("Part 1", len(visibleTrees))

# PART 2
# Strategy: let's iterate again over all trees ¯\_(ツ)_/¯

bestScenicScoreYet = 0

# We can discard the edge because the scenic score is always 0
# (so +1 and -1 in the range bounds)


def isInGrid(x, y):
    return x >= 0 and x < width and y >= 0 and y < height


def getViewingDistance(grid, x, y, direction):
    assert isInGrid(x, y)
    treeHeight = grid[y][x]
    currentDistance = 0
    curX, curY = x + direction[0], y + direction[1]
    while isInGrid(curX, curY):
        currentDistance += 1
        if grid[curY][curX] >= treeHeight:
            break
        curX += direction[0]
        curY += direction[1]

    return currentDistance


for y in range(1, height - 1):
    for x in range(1, width - 1):
        dirRight = getViewingDistance(data, x, y, (1, 0))
        dirLeft = getViewingDistance(data, x, y, (-1, 0))
        dirTop = getViewingDistance(data, x, y, (0, 1))
        dirBottom = getViewingDistance(data, x, y, (0, -1))

        scenicScore = dirRight * dirLeft * dirTop * dirBottom
        if scenicScore > bestScenicScoreYet:
            bestScenicScoreYet = scenicScore

print("PArt 2", bestScenicScoreYet)
