from collections import defaultdict, deque
from typing import DefaultDict, List, Set, Tuple

from icecream import ic

Node = Tuple[int, int]
Grid = List[List[int]]


DIR_OFFSETS: Tuple[Node, ...] = [(0, 1), (1, 0), (0, -1), (-1, 0)]


def get_valid_neighbours(data: Grid, x: int, y: int) -> Tuple[Node, ...]:
    # Get valid neighboring nodes that are reachable from the current position.

    width, height = len(data[0]), len(data)
    current_value = data[y][x]

    neighbours = {
        (new_x, new_y)
        for dx, dy in DIR_OFFSETS
        if (new_x := x + dx) in range(width)
        and (new_y := y + dy) in range(height)
        and data[new_y][new_x] == current_value + 1
    }

    return tuple(neighbours)


def parse_topo_map(
    string_map: str,
) -> Tuple[Grid, DefaultDict[Node, Set[Node]], List[Node]]:
    topo_grid = [
        [int(digit) for digit in line.strip()] for line in string_map.split("\n")
    ]

    adjacency_list = defaultdict(set)
    starting_positions = []

    for y, row in enumerate(topo_grid):
        for x, height in enumerate(row):
            coord = (x, y)
            if height == 0:
                starting_positions.append(coord)
            adjacency_list[coord].update(get_valid_neighbours(topo_grid, *coord))

    return topo_grid, adjacency_list, starting_positions


def score(
    grid: Grid,
    graph: DefaultDict[Node, Set[Node]],
    start_node: Node,
    distinct: bool = False,
):
    # Basically just BFS - Path starts at 0 and ends at a node with value 9
    seen = set()
    queue = deque([start_node])
    trailhead_score = 0

    while queue:
        current_node = queue.popleft()
        current_height = grid[current_node[1]][current_node[0]]

        if distinct or current_node not in seen:
            seen.add(current_node)

            if current_height == 9:
                trailhead_score += 1
            else:
                queue.extend(graph[current_node])

    return trailhead_score


with open("input.txt") as f:
    topo_map, graph, start_nodes = parse_topo_map(f.read())


total_score = 0
for start_node in start_nodes:
    # The score function now sets the distinct flag to True for Part 2.
    # Fun fact: My initial (wrong) solution for Part 1 was the correct solution for Part 2.
    total_score += score(topo_map, graph, start_node, distinct=True)

ic(
    f"The sum of the ratings of all trailheads (based on distinct trails): {total_score}"
)
