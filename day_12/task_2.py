from collections import deque
from typing import List, Set, Tuple

from icecream import ic

Node = Tuple[int, int]
Grid = List[List[str]]

DIRECTIONS: Tuple[Node, ...] = [(1, 0), (-1, 0), (0, 1), (0, -1)]


def is_valid_position(pos: Node, grid: Grid) -> bool:
    x, y = pos
    return 0 <= x < len(grid[0]) and 0 <= y < len(grid)


def apply_direction(node: Node, dir_idx: int) -> Node:
    x, y = node
    dx, dy = DIRECTIONS[dir_idx]
    return (x + dx, y + dy)


def count_corners(plot: Node, region: Set[Node]) -> int:
    """
    TLDR:

    Outer Corners:           Inner Corners:
    (X = corner, # = plant)  (X = corner, # = plant)

    1)  X.     2)  .X        5)  ##     6)  ##
        .#         #.            #X         X#

    3)  .#     4)  #.        7)  ##     8)  ##
        X.         .X            X#         #X
    
    """

    corners = 0

    # Check outer corners
    for i, j in [(0, 2), (0, 3), (1, 2), (1, 3)]:
        if (
            apply_direction(plot, i) not in region
            and apply_direction(plot, j) not in region
        ):
            corners += 1

    # Check inner corners
    for i, j in [(0, 2), (0, 3), (1, 2), (1, 3)]:
        if (
            apply_direction(plot, i) in region
            and apply_direction(plot, j) in region
            and apply_direction(apply_direction(plot, i), j) not in region
        ):
            corners += 1

    return corners


def analyze_region(plant: str, start: Node, grid: Grid) -> Tuple[int, Set[Node]]:
    plots: Set[Node] = set()
    queue = deque([start])

    while queue:
        current = queue.popleft()
        if current in plots:
            continue

        x, y = current
        if grid[y][x] == plant:
            plots.add(current)

            for dir_idx, _ in enumerate(DIRECTIONS):
                next_pos = apply_direction(current, dir_idx)
                if (
                    next_pos not in plots
                    and is_valid_position(next_pos, grid)
                    and grid[next_pos[1]][next_pos[0]] == plant
                ):
                    queue.append(next_pos)

    corners = sum(count_corners(plot, plots) for plot in plots)

    return (len(plots) * corners), plots


def calculate_price(grid: Grid) -> int:
    seen: Set[Node] = set()
    total_price = 0

    for y, row in enumerate(grid):
        for x, plant in enumerate(row):
            current = (x, y)
            if current not in seen:
                price, plots = analyze_region(plant, current, grid)
                ic(f"Plant: {plant}, Price: {price}")
                total_price += price
                seen.update(plots)

    return total_price


with open("input.txt") as file:
    grid = [list(line.strip()) for line in file]

result = calculate_price(grid)
ic(f"Total price: {result}")
