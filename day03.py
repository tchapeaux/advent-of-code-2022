import aoc

data = aoc.getLinesForDay(3)

PRIO = "_abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


def getPriorityOf(objectType):
    return PRIO.index(objectType)


accPart1 = 0
for line in data:
    assert len(line) % 2 == 0
    middleIdx = int(len(line) / 2)
    firstBag = line[:middleIdx]
    secondBag = line[middleIdx:]

    # find common type
    firstBagTypes = set(firstBag)
    secondBagTypes = set(secondBag)
    commonTypes = firstBagTypes.intersection(secondBagTypes)
    assert len(commonTypes) == 1
    commonType = commonTypes.pop()

    accPart1 += getPriorityOf(commonType)

print("Part 1", accPart1)

accPart2 = 0
assert len(data) % 3 == 0

for idx in range(int(len(data) / 3)):
    elf1Types = set(data[3 * idx])
    elf2Types = set(data[3 * idx + 1])
    elf3Types = set(data[3 * idx + 2])

    print(data[idx])
    print(data[idx + 1])
    print(data[idx + 2])

    commonTypes = elf1Types.intersection(elf2Types).intersection(elf3Types)
    assert len(commonTypes) == 1, commonTypes
    commonType = commonTypes.pop()
    print(commonType)

    accPart2 += getPriorityOf(commonType)

print("Part 2", accPart2)
