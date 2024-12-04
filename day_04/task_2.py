from enum import Enum
from itertools import product
from typing import List, Tuple

from icecream import ic

# Type aliases for better readability
Position = Tuple[int, int]
PositionSequence = Tuple[Position, ...]
SearchResult = List[PositionSequence]


class Direction(Enum):
    BOTTOM_LEFT_TO_TOP_RIGHT = 1
    TOP_LEFT_TO_BOTTOM_RIGHT = 2


# TODO: Instead of going diagonally, we could instead shift the grid and search horizontally and vertically. This would be more efficient.
def search_diagonally(grid: list[str], direction: Direction, word: str) -> SearchResult:
    """Search for a word in a grid diagonally. Either from bottom left to top right or top left to bottom right.
    Return a list of tuples where each tuple contains the row and column of each letter in the word.
    e.g. [((0, 0), (1, 1), (2, 2)), ((0, 1), (1, 2), (2, 3))]
    """

    result = []

    # This is a more generic solution that stores the positions of every letter in the word
    # In our case we could simply opt for only storing the middle letter A

    if direction == Direction.BOTTOM_LEFT_TO_TOP_RIGHT:
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                if i + len(word) <= len(grid) and j + len(word) <= len(grid[0]):
                    if "".join([grid[i + k][j + k] for k in range(len(word))]) == word:
                        result.append(tuple((i + k, j + k) for k in range(len(word))))
    else:
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                if i - len(word) >= -1 and j + len(word) <= len(grid[0]):
                    if "".join([grid[i - k][j + k] for k in range(len(word))]) == word:
                        result.append(tuple((i - k, j + k) for k in range(len(word))))

    return result


def search_word(grid: list[str], word: str) -> tuple[SearchResult, SearchResult]:
    sd_bl = search_diagonally(grid, Direction.BOTTOM_LEFT_TO_TOP_RIGHT, word)
    sd_tl = search_diagonally(grid, Direction.TOP_LEFT_TO_BOTTOM_RIGHT, word)

    return (sd_bl, sd_tl)


with open("input.txt") as f:
    grid = f.read().splitlines()

# Return search results by searching diagonally for the words 'MAS' and 'SAM' (bl = bottom left, tl = top left)
xmas_bl, xmas_tl = search_word(grid, "MAS")
samx_bl, samx_tl = search_word(grid, "SAM")

match_count = 0
bls = [xmas_bl, samx_bl]
tls = [xmas_tl, samx_tl]

for bl, tl in product(bls, tls):
    # mas and mas/sam must share the same A position if they cross each other
    bottom_a = {entry[1] for entry in bl}  # Second position of each tuple
    top_a = {entry[1] for entry in tl}

    match_count += len(bottom_a & top_a)

ic(f"X-MAS appears {match_count} times in the grid.")
