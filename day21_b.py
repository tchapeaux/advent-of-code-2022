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

# Apply correction
monkeys["root"] = (monkeys["root"][0], "=", monkeys["root"][2])
monkeys["humn"] = "x"
monkeysThatYelled.remove("humn")

# Check data integrity
assert "root" in monkeyNames
for monkeyName in monkeys.keys():
    if monkeyName != "humn" and monkeyName not in monkeysThatYelled:
        rule = monkeys[monkeyName]
        assert rule[0] in monkeyNames
        assert rule[2] in monkeyNames

# Simulate yelling 📢 to simplify as much as possible
hasProgressed = True
while hasProgressed:
    hasProgressed = False
    for m in monkeyNames:
        if m in monkeysThatYelled:
            continue
        if m == "humn":
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


# Unwrap the rule into a single expression


def unwrapRule(rule):
    if type(rule) == int:
        return rule
    if rule == "x":
        return "x"

    op1 = rule[0]
    operator = rule[1]
    op2 = rule[2]
    assert operator in "+-*/="

    newOp1 = unwrapRule(monkeys[op1])
    newOp2 = unwrapRule(monkeys[op2])

    return f"({newOp1} {operator} {newOp2})"


rootRule = monkeys["root"]
print("Math equation to solve:")
print(unwrapRule(rootRule)[1:-1])

# I didn't want to write an algebra solver
# so I copy-pasted the equation to this website
# https://www.mathpapa.com/equation-solver/
# and it gave me the answer :)
