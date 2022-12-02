import aoc

ROCK = "A"
PAPER = "B"
SCISSOR = "C"


def getOutcome(myMove, opponentMove):
    if myMove == opponentMove:
        return 3

    if myMove == ROCK and opponentMove == SCISSOR:
        return 6
    if myMove == SCISSOR and opponentMove == PAPER:
        return 6
    if myMove == PAPER and opponentMove == ROCK:
        return 6

    return 0


def getScore(myMove, opponentMove):
    score = 0
    if myMove == ROCK:
        score += 1
    if myMove == PAPER:
        score += 2
    if myMove == SCISSOR:
        score += 3

    score += getOutcome(myMove, opponentMove)
    return score


def translateMySymbolPart1(mySymbol):
    translateDict = dict(X="A", Y="B", Z="C")
    return translateDict[mySymbol]


def translateMySymbolPart2(mySymbol, opponentMove):
    if mySymbol == "Y":
        return opponentMove

    if mySymbol == "X":
        loseDict = dict(A="C", B="A", C="B")
        return loseDict[opponentMove]

    if mySymbol == "Z":
        winDict = dict(A="B", B="C", C="A")
        return winDict[opponentMove]


data = aoc.getLinesForDay(2)

cumulativeSum1 = 0
cumulativeSum2 = 0
for line in data:
    [opponentMove, mySymbol] = line.split(" ")

    myMove1 = translateMySymbolPart1(mySymbol)
    cumulativeSum1 += getScore(myMove1, opponentMove)

    myMove2 = translateMySymbolPart2(mySymbol, opponentMove)
    print(myMove2, opponentMove)
    cumulativeSum2 += getScore(myMove2, opponentMove)


print("Part 1", cumulativeSum1)
print("Part 2", cumulativeSum2)

# Part 2 10318 too low (swapped the order of winDict and loseDict)
