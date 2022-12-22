import aoc

data = aoc.getLinesForDay(21)

monkeys = {}
monkeyNames = set()
monkeysThatYelled = set()
for line in data:
    monkeyName, monkeyRule = line.strip().split(": ")
    monkeyNames.add(monkeyName)
    if monkeyRule.isdigit():
        monkeys[monkeyName] = int(monkeyRule)
        monkeysThatYelled.add(monkeyName)
    else:
        rule = monkeyRule.split(" ")
        assert len(rule) == 3
        assert rule[1] in "+-*/"
        monkeys[monkeyName] = tuple(rule)


# Check data integrity
assert "root" in monkeyNames
for monkeyName in monkeys.keys():
    if monkeyName not in monkeysThatYelled:
        rule = monkeys[monkeyName]
        assert rule[0] in monkeyNames
        assert rule[2] in monkeyNames

# Simulate yelling 📢
while "root" not in monkeysThatYelled:
    hasProgressed = False
    for m in monkeyNames:
        if m in monkeysThatYelled:
            continue

        rule = monkeys[m]
        op1 = rule[0]
        operator = rule[1]
        op2 = rule[2]
        if op1 in monkeysThatYelled and op2 in monkeysThatYelled:
            result = 0
            if operator == "+":
                result = monkeys[op1] + monkeys[op2]
            elif operator == "-":
                result = monkeys[op1] - monkeys[op2]
            elif operator == "*":
                result = monkeys[op1] * monkeys[op2]
            elif operator == "/":
                result = monkeys[op1] / monkeys[op2]
            monkeys[m] = int(result)
            monkeysThatYelled.add(m)
            hasProgressed = True

print("Part 1", monkeys["root"])
