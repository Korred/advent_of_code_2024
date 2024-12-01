from icecream import ic

with open("input.txt", "r") as file:
    list_a, list_b = map(sorted, zip(*(map(int, line.split()) for line in file)))

distance = sum(abs(a - b) for a, b in zip(list_a, list_b))

ic("The total distance between the lists is:", distance)
