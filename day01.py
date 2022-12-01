import aoc

data = aoc.getLinesForDay(1)

""" example data
data = [
    "1000",
    "2000",
    "3000",
    "",
    "4000",
    "",
    "5000",
    "6000",
    "",
    "7000",
    "8000",
    "9000",
    "",
    "10000",
]
"""

elves = []
currentElfValue = 0

for line in data:
    if len(line) > 0:
        currentElfValue += int(line)
    else:
        elves.append(currentElfValue)
        currentElfValue = 0

elves = sorted(elves)


# Part 1 69893 too low (typed too fast and forgot to sum())
print("Part 1", elves[-1])
print("Part 2", sum([elves[-1], elves[-2], elves[-3]]))
