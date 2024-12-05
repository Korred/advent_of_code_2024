from collections import defaultdict
from icecream import ic


def create_rules_lookup(rules):
    rules_lookup = defaultdict(list)
    for rule in rules.split("\n"):
        left, right = map(int, rule.split("|"))

        rules_lookup[left].append(("<", right))
        rules_lookup[right].append((">", left))

    return rules_lookup


def prepare_updates(updates):
    updates = updates.split("\n")
    return [list(map(int, update.split(","))) for update in updates]


def is_valid_update(update, rules_lookup):
    for i, page_a in enumerate(update):
        for direction, page_b in rules_lookup[page_a]:
            if (direction == "<" and page_b in update[:i]) or (
                direction == ">" and page_b in update[i + 1 :]
            ):
                return False

    return True


with open("input.txt") as file:
    rules, updates = file.read().split("\n\n")

rules_lookup = create_rules_lookup(rules)
updates = prepare_updates(updates)
valid_updates = [update for update in updates if is_valid_update(update, rules_lookup)]

# Get the middle number of each update entry
middle_numbers = [page[len(page) // 2] for page in valid_updates]

ic(
    f"The sum of all middle page numbers for all valid updates is: {sum(middle_numbers)}"
)
