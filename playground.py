# Playground file
# This is just for small experiments during the jam
# Mostly useful for me when I forget what the exact Python syntax for something is

import aoc
import re

print("hello there")

aoc.getInputForDay(1)


print(re.search(r"x*", "xxxx"))

listOfList = [[0, 0] for _ in range(4)]
listOfList[0][1] = 1
print(listOfList)

findNumbersRegex = r"(-?\d+)"
print(
    re.findall(
        findNumbersRegex, "Sensor at x=12, y=14: closest beacon is at x=-10, y=16"
    )
)

a = (53, "ABC")
b = (2, "DEF")
c = (2, "A")

print(tuple(sorted([a, b, c])))
