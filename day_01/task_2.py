from collections import Counter

from icecream import ic

with open("input.txt", "r") as file:
    list_a, list_b = map(sorted, zip(*(map(int, line.split()) for line in file)))

counter_b = Counter(list_b)

similiarity_score = sum(a * counter_b[a] for a in list_a)
ic("The similiarity score between the lists is:", similiarity_score)
