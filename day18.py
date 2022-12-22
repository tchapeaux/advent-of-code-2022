import math

import aoc

data = aoc.getLinesForDay(18)
# data = aoc.getLinesForDay(18, force_filepath="inputs/day18_example.txt")

inputCubes = set()
for line in data:
    inputCubes.add(tuple([int(x) for x in line.split(",")]))

print(len(inputCubes), "cubes")

all_x = set([c[0] for c in inputCubes])
all_y = set([c[1] for c in inputCubes])
all_z = set([c[2] for c in inputCubes])
print(
    "GRID DIMENSION",
    min(all_x),
    max(all_x),
    min(all_y),
    max(all_y),
    min(all_z),
    max(all_z),
)


def isAdjacent(cube1, cube2):
    return (
        abs(cube1[0] - cube2[0]) + abs(cube1[1] - cube2[1]) + abs(cube1[2] - cube2[2])
        == 1
    )


accSurface = 0
for cube1 in inputCubes:
    nbOfAdj = 0
    for cube2 in inputCubes:
        if isAdjacent(cube1, cube2):
            nbOfAdj += 1

    accSurface += 6 - nbOfAdj

print("Part 1", accSurface)

# 16354 too high : typo in the number of faces of a cube (12 instead of 6)

# Part 2


def get6Neighbors(cube):
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            for dz in [-1, 0, 1]:
                if abs(dx) + abs(dy) + abs(dz) == 1:
                    yield (cube[0] + dx, cube[1] + dy, cube[2] + dz)


def isOutOfBounds(cube):
    return (
        cube[0] < min(all_x)
        or cube[0] > max(all_x)
        or cube[1] < min(all_y)
        or cube[1] > max(all_y)
        or cube[2] < min(all_z)
        or cube[2] > max(all_z)
    )


def isOutwardFace(cube, neighbor):
    # Strategy: bucket fill until we either reach the edge or we stop
    # If we reach the edge -> outward-facing face
    # If not and we can't continue filling -> inward-facing face or adjacent face
    assert isAdjacent(cube, neighbor)
    if neighbor in inputCubes:
        return False
    frontier = set([neighbor])
    visited = set()
    # print("\t", len(frontier), len(visited))
    while len(frontier) > 0:
        currentCube = frontier.pop()
        if isOutOfBounds(currentCube):
            return True
        for neigh in get6Neighbors(currentCube):
            if neigh in visited or neigh in inputCubes:
                continue
            frontier.add(neigh)
        visited.add(currentCube)
    # Frontier is empty and no out of bound was found
    return False


def countOutwardFaces(cube):
    accOutFaces = 0
    for neigh in get6Neighbors(cube):
        if neigh not in inputCubes:
            if isOutwardFace(cube, neigh):
                accOutFaces += 1
    return accOutFaces


accOutSurface = 0
for cubeIdx, cube in enumerate(inputCubes):
    print(cubeIdx + 1, "/", len(inputCubes))
    accOutSurface += countOutwardFaces(cube)

print("Part 2", accOutSurface)
