import aoc

data = aoc.getLinesForDay(10)
# data = aoc.getLinesForDay(10, force_filepath="inputs/day10_small_example.txt")
# data = aoc.getLinesForDay(10, force_filepath="inputs/day10_example.txt")

interestingSignalStrengths = []  # 20, 60, 100, 140, 180, 220
registerX = 1
cycle = 0
crtScreen = [[]]


def doEachCycleComputation():
    currentRow = crtScreen[-1]
    pixelDrawnPosition = len(currentRow)
    spriteMiddle = registerX
    deltaDistance = abs(spriteMiddle - pixelDrawnPosition)
    currentRow.append("#" if deltaDistance <= 1 else ".")

    if cycle % 40 == 20:
        interestingSignalStrengths.append(cycle * registerX)

    if cycle % 40 == 0 and cycle > 0:
        crtScreen.append([])


# Intepret the instructions one by one
for instr in data:
    if instr == "noop":
        cycle += 1
        doEachCycleComputation()
    elif instr.startswith("addx"):
        param = int(instr.split(" ")[1])
        cycle += 1
        doEachCycleComputation()
        cycle += 1
        doEachCycleComputation()
        registerX += param

    # print("cycle", cycle, "value", registerX)


print("Part 1", sum(interestingSignalStrengths))

# 13900 too low because my registerX started at 0 instead of 1

print("Part 2")
for row in crtScreen:
    print("".join(row))

# BJRFHRFU <- mixed 2 letters because apparently I can't read
# BJFRHRFU
