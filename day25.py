import math
from typing import Dict

import aoc

data = aoc.getLinesForDay(25)

SNAFU_DIGITS: Dict[str, int] = {"2": 2, "1": 1, "0": 0, "-": -1, "=": -2}


def snafuToInt(snafu: str) -> int:
    acc = 0
    for place, d in enumerate(reversed(snafu)):
        acc += SNAFU_DIGITS[d] * math.pow(5, place)
    return int(acc)


assert snafuToInt("1=") == 3
assert snafuToInt("1=11-2") == 2022
assert snafuToInt("1-0---0") == 12345
assert snafuToInt("1121-1110-1=0") == 314159265


# Function to convert base10 to "normal" base5
# Source: https://stackoverflow.com/a/66481189
def changebase(n, base=10, to=10):
    """
    params:
      n     - number to convert
      base  - current base of number 'n'
      to    - desired base, must be <= 36
    """
    # check that new base is <= 36
    if to > 36 or base > 36:
        raise ValueError("max base is 36")

    # convert to base 10
    n = int(str(n), base)
    positive = n >= 0

    # return if base 10 is desired
    if to == 10:
        return str(n)

    # convert to new base
    n = abs(n)
    num = []
    handle_digit = lambda n: str(n) if n < 10 else chr(n + 55)
    while n > 0:
        num.insert(0, handle_digit(n % to))
        n = n // to

    # return string value of n in new base
    return "".join(num) if positive else "-" + "".join(num)


def intToSnafu(myInt: int) -> str:
    intBase5 = "0" + changebase(myInt, 10, 5)

    # Strategy: replace all 3 by "1=" and all 4 by "1-" and all 5 by "10"

    for digIdx in range(len(intBase5))[::-1]:
        if intBase5[digIdx] == "3":
            intBase5 = intBase5[:digIdx] + "=" + intBase5[digIdx + 1 :]
            intBase5 = (
                intBase5[: digIdx - 1]
                + str(int(intBase5[digIdx - 1]) + 1)
                + intBase5[digIdx:]
            )

        if intBase5[digIdx] == "4":
            intBase5 = intBase5[:digIdx] + "-" + intBase5[digIdx + 1 :]
            intBase5 = (
                intBase5[: digIdx - 1]
                + str(int(intBase5[digIdx - 1]) + 1)
                + intBase5[digIdx:]
            )

        if intBase5[digIdx] == "5":
            intBase5 = intBase5[:digIdx] + "0" + intBase5[digIdx + 1 :]
            intBase5 = (
                intBase5[: digIdx - 1]
                + str(int(intBase5[digIdx - 1]) + 1)
                + intBase5[digIdx:]
            )

    if intBase5[0] == "0":
        intBase5 = intBase5[1:]

    return intBase5


assert intToSnafu(2022) == "1=11-2"
assert intToSnafu(12345) == "1-0---0"
assert intToSnafu(314159265) == "1121-1110-1=0"

accPart1 = 0
for line in data:
    accPart1 += snafuToInt(line)

print("Part1", intToSnafu(accPart1))
