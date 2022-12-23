from enum import Enum
import copy
from typing import Dict, Optional, Tuple, List, Set
import re

import aoc

data = aoc.getLinesForDay(19)
data = aoc.getLinesForDay(19, force_filepath="inputs/day19_example.txt")

# Enums and types

Minute = int
Score = int


class Robots(Enum):
    ORE = "ROBOT_ORE"
    CLAY = "ROBOT_CLAY"
    OBS = "ROBOT_OBS"
    GEO = "ROBOT_GEO"


class Resources(Enum):
    ORE = "RESOURCE_ORE"
    CLAY = "RESOURCE_CLAY"
    OBS = "RESOURCE_OBS"
    GEO = "RESOURCE_GEO"


Blueprint = Dict[Robots, Dict[Resources, int]]

CurrentResources = Dict[Resources, int]
CurrentRobots = Dict[Robots, int]
State = Tuple[Minute, Tuple[Tuple[Resources, int]], Tuple[Tuple[Robots, int]]]


RESOURCE_TO_ROBOT = {
    Resources.ORE: Robots.ORE,
    Resources.CLAY: Robots.CLAY,
    Resources.OBS: Robots.OBS,
    Resources.GEO: Robots.GEO,
}

MAX_MINUTE = 21

# Parse

blueprints: List[Blueprint] = []
PARSE_REGEX = r"Blueprint (\d+): Each ore robot costs (\d+) ore. Each clay robot costs (\d+) ore. Each obsidian robot costs (\d+) ore and (\d+) clay. Each geode robot costs (\d+) ore and (\d+) obsidian."
for line in data:
    m = re.match(PARSE_REGEX, line)
    assert m is not None
    (
        blueprintIdx,
        oreRobotOreCost,
        clayRobotOreCost,
        obsidianRobotOreCost,
        obisdianRobotClayCost,
        geodeRobotOreCost,
        geodeRobotObisidianCost,
    ) = m.groups()
    blueprints.append(
        {
            Robots.ORE: {Resources.ORE: int(oreRobotOreCost)},
            Robots.CLAY: {Resources.ORE: int(clayRobotOreCost)},
            Robots.OBS: {
                Resources.ORE: int(obsidianRobotOreCost),
                Resources.CLAY: int(obisdianRobotClayCost),
            },
            Robots.GEO: {
                Resources.ORE: int(geodeRobotOreCost),
                Resources.OBS: int(geodeRobotObisidianCost),
            },
        }
    )


def printState(state: State):
    print(state[0], [t[1] for t in state[1]], [t[1] for t in state[2]])


class Simulator:
    def __init__(self, blueprint: Blueprint):
        self.blueprint: Blueprint = blueprint
        self.maxMinute: Minute = MAX_MINUTE

        self.currentBest: int = 0
        self.knownStates: set[State] = set()
        self.bestScorePerMinute: Dict[Minute, List[int]] = {}
        self.resToScore = {}
        self.robToScore = {}
        self.nbOfAlreadySeenStates = 0
        self.nbOfLessGoodScore = 0

    def findBestOutcome(self) -> int:
        resources: CurrentResources = {
            Resources.ORE: 0,
            Resources.CLAY: 0,
            Resources.OBS: 0,
            Resources.GEO: 0,
        }
        robots: CurrentRobots = {
            Robots.ORE: 1,
            Robots.CLAY: 0,
            Robots.OBS: 0,
            Robots.GEO: 0,
        }

        self.knownStates: Set[State] = set()
        for m in range(self.maxMinute):
            self.bestScorePerMinute[m + 1] = []
        self.generateScoreMaps()
        self.nbOfAlreadySeenStates = 0
        self.nbOfLessGoodScore = 0

        return self.exploreSteps(1, resources, robots)

    def getChoices(self, resources: Dict[Resources, int]) -> List[Optional[Robots]]:
        choices: List[Optional[Robots]] = []
        for robot in self.blueprint.keys():
            hasEnough = True
            for requiredResource in self.blueprint[robot].keys():
                if (
                    resources[requiredResource]
                    < self.blueprint[robot][requiredResource]
                ):
                    hasEnough = False
            if hasEnough:
                choices.append(robot)
        choices.append(None)

        # Force to build a GEO robot when possible
        if Robots.GEO in choices:
            return [Robots.GEO]

        return choices

    def generateScoreMaps(self):
        resToScore = {}
        resToScore[Resources.ORE] = 1
        resToScore[Resources.CLAY] = self.blueprint[Robots.CLAY][Resources.ORE]
        resToScore[Resources.OBS] = (
            self.blueprint[Robots.OBS][Resources.ORE]
            + resToScore[Resources.CLAY] * self.blueprint[Robots.OBS][Resources.CLAY]
        )
        resToScore[Resources.GEO] = (
            self.blueprint[Robots.GEO][Resources.ORE]
            + resToScore[Resources.OBS] * self.blueprint[Robots.GEO][Resources.OBS]
        )
        self.resToScore = resToScore

        robToScore = {}
        robToScore[Robots.ORE] = self.blueprint[Robots.ORE][Resources.ORE]
        robToScore[Robots.CLAY] = self.blueprint[Robots.CLAY][Resources.ORE]
        robToScore[Robots.OBS] = (
            self.blueprint[Robots.OBS][Resources.ORE]
            + self.blueprint[Robots.OBS][Resources.CLAY] * resToScore[Resources.CLAY]
        )
        robToScore[Robots.GEO] = (
            self.blueprint[Robots.GEO][Resources.ORE]
            + self.blueprint[Robots.GEO][Resources.OBS] * resToScore[Resources.OBS]
        )
        self.robToScore = robToScore

    def getScore(self, resources, robots) -> Score:
        # We count the number of generated ore equivalent
        score = 0
        score += sum([resources[res] * self.resToScore[res] for res in Resources])
        score += sum([robots[rob] * self.robToScore[rob] for rob in Robots])
        return score

    def exploreSteps(
        self,
        currentMinute: Minute,
        resources: Dict[Resources, int],
        robots: Dict[Robots, int],
    ) -> int:
        newRobotChoices = self.getChoices(resources)

        newResources = {}
        for res in Resources:
            newResources[res] = resources[res] + robots[RESOURCE_TO_ROBOT[res]]

        currentGeo = newResources[Resources.GEO]

        if currentMinute == self.maxMinute:
            return currentGeo

        state: State = (
            currentMinute,
            tuple(newResources.items()),
            tuple(robots.items()),
        )

        # printState(state)
        # print(len(self.knownStates))
        if state in self.knownStates:
            self.nbOfAlreadySeenStates += 1
            # print("Already seen", len(self.knownStates), self.nbOfAlreadySeenStates)
            return 0
        self.knownStates.add(state)

        # Compare this state to the best known state at the same minute
        # we compare state based on the total number of earned resources
        currentScore: Score = self.getScore(newResources, robots)
        bestKnownScore = self.bestScorePerMinute[currentMinute]
        if len(bestKnownScore) >= 2 and currentScore < min(bestKnownScore):
            self.nbOfLessGoodScore += 1
            print("less good score", currentMinute, self.nbOfLessGoodScore)
            return 0
        bestKnownScore.append(currentScore)
        self.bestScorePerMinute[currentMinute] = sorted(bestKnownScore)

        # Find upper bound of expected gain
        # in order to stop early if possible

        for newRobotChoice in newRobotChoices:

            choiceResources = copy.copy(newResources)
            newRobots = copy.copy(robots)

            if newRobotChoice is not None:
                newRobots[newRobotChoice] += 1

                for res in blueprint[newRobotChoice].keys():
                    choiceResources[res] -= blueprint[newRobotChoice][res]
                    assert choiceResources[res] >= 0

            expectedGain = self.exploreSteps(
                currentMinute + 1, choiceResources, newRobots
            )
            if expectedGain > self.currentBest:
                self.currentBest = expectedGain

        return self.currentBest


# Part 1

accPart1 = 0
for blueprintIdx, blueprint in enumerate(blueprints):
    sim = Simulator(blueprint)
    bestOutcome = sim.findBestOutcome()
    print(blueprintIdx + 1, bestOutcome)
    accPart1 += (blueprintIdx + 1) * bestOutcome

print("Part 1", accPart1)
print("Found in", aoc.getTick())
