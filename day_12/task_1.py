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


def analyze_region(
    plant: str, node: Node, data: list[list[str]]
) -> tuple[int, set[Node]]:
    plots = 0
    sides = 0
    seen: Set[Node] = set()
    queue = deque([node])

    while queue:
        current = queue.popleft()
        if current in seen:
            continue

        x, y = current
        if data[y][x] == plant:
            seen.add(current)
            plots += 1

            for dir_idx, _ in enumerate(DIRECTIONS):
                next_pos = apply_direction(current, dir_idx)

                if next_pos not in seen:
                    if is_valid_position(next_pos, grid):
                        nx, ny = next_pos
                        if data[ny][nx] == plant:
                            queue.append((nx, ny))
                        else:
                            sides += 1
                    else:
                        sides += 1

    return (plots * sides, set(seen))


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
