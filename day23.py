from typing import Tuple, List, Dict

import aoc

data = aoc.getCellsForDay(23)
# data = aoc.getCellsForDay(23, force_filepath="inputs/day23_example.txt")
# data = aoc.getCellsForDay(23, force_filepath="inputs/day23_mini_example.txt")

Position = Tuple[int, int]

PROPOSAL_ORDER: Dict[Position, Tuple[Position, Position, Position]] = {
    (0, -1): ((-1, -1), (0, -1), (1, -1)),
    (0, 1): ((-1, 1), (0, 1), (1, 1)),
    (-1, 0): ((-1, -1), (-1, 0), (-1, 1)),
    (1, 0): ((1, -1), (1, 0), (1, 1)),
}

initialPositions: List[Position] = []
for y in range(len(data)):
    for x in range(len(data[y])):
        if data[y][x] == "#":
            initialPositions.append((x, y))


def getProposedPositions(positions, roundIdx) -> List[Position]:
    proposedPositions = []
    for (x, y) in positions:
        # print("check", (x, y))
        proposedPos = (x, y)

        # Check 8 neighbors
        hasNeigh = any(
            [
                (x + dx, y + dy) in positions
                for dx in (-1, 0, 1)
                for dy in (-1, 0, 1)
                if not (dx == dy == 0)
            ]
        )

        if hasNeigh:
            firstProposalIdx = roundIdx % len(PROPOSAL_ORDER)
            for proposalOffset in range(len(PROPOSAL_ORDER)):
                proposalIdx = (firstProposalIdx + proposalOffset) % len(PROPOSAL_ORDER)
                proposalNewPos, proposalTargets = list(PROPOSAL_ORDER.items())[
                    proposalIdx
                ]
                # print("\tchecking", proposalNewPos)
                for (dx, dy) in proposalTargets:
                    targetPos = (x + dx, y + dy)
                    if targetPos in positions:
                        # print("\t\tbreak")
                        break
                else:
                    proposedPos = (x + proposalNewPos[0], y + proposalNewPos[1])
                    break

        # print("Proposed =>", proposedPos)
        proposedPositions.append(proposedPos)

    return proposedPositions


def getGridStr(positions):
    all_x = set(pos[0] for pos in positions)
    all_y = set(pos[1] for pos in positions)
    min_x = min(all_x)
    max_x = max(all_x)
    min_y = min(all_y)
    max_y = max(all_y)

    gridStr = f"{(min_x, min_y)}" + "\n"
    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            if (x, y) in positions:
                gridStr += "#"
            else:
                gridStr += "."
        gridStr += "\n"
    return gridStr


print("Initial")
print(getGridStr(initialPositions))

currentPosition: List[Position] = [p for p in initialPositions]
round = 0
while True:
    print("round", round + 1)
    tentativePositions: List[Position] = getProposedPositions(currentPosition, round)

    # Only confirm the unique positions
    newPositions: List[Position] = []
    for elfIdx, position in enumerate(tentativePositions):
        if tentativePositions.count(position) > 1:
            newPositions.append(currentPosition[elfIdx])
        else:
            newPositions.append(tentativePositions[elfIdx])

    # print(getGridStr(newPositions))

    if set(currentPosition) == set(newPositions):
        print("No elf moved!")
        print("Part 2", round + 1)
        break
    currentPosition = newPositions

    # Part 1 end condition at round 10
    if round == 9:
        part1FinalPosition = currentPosition

        all_x = set(pos[0] for pos in part1FinalPosition)
        all_y = set(pos[1] for pos in part1FinalPosition)
        min_x = min(all_x)
        max_x = max(all_x)
        min_y = min(all_y)
        max_y = max(all_y)

        area = (max_x - min_x + 1) * (max_y - min_y + 1)
        print("Part 1", area - len(part1FinalPosition))

        # 3730 (too low)

    round += 1
