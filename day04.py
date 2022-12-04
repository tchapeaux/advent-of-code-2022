import aoc

data = aoc.getLinesForDay(4)


def isContained(range1, range2):
    if range1[0] <= range2[0] and range1[1] >= range2[1]:
        return True

    if range2[0] <= range1[0] and range2[1] >= range1[1]:
        return True

    return False


def doOverlap(range1, range2):
    if isContained(range1, range2):
        return True

    # if no intersection => false
    if range1[1] < range2[0] or range2[1] < range1[0]:
        return False

    # All other cases are intersections
    return True


assert doOverlap([42, 65], [50, 67])

accPart1 = 0
accPart2 = 0
for line in data:
    print(line)
    eachPair = line.split(",")
    elf1Range = [int(x) for x in eachPair[0].split("-")]
    elf2Range = [int(x) for x in eachPair[1].split("-")]
    assert elf1Range[0] <= elf1Range[1]
    assert elf2Range[0] <= elf2Range[1], elf2Range

    if isContained(elf1Range, elf2Range):
        accPart1 += 1

    if doOverlap(elf1Range, elf2Range):
        accPart2 += 1


print("Part 1", accPart1)
print("Part 2", accPart2)
