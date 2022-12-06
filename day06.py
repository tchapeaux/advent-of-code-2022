import aoc

data = aoc.getInputForDay(6)


totalLength = len(data)


def findFirstDistinct(nbOfChars):
    for i in range(totalLength - nbOfChars):
        substr = data[i : i + nbOfChars]

        # print(i, substr)

        if len(set(substr)) == nbOfChars:
            return i + nbOfChars


print("Part 1", findFirstDistinct(4))
print("Part 2", findFirstDistinct(14))
