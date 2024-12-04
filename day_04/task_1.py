from enum import Enum

from icecream import ic


class Direction(Enum):
    BOTTOM_LEFT_TO_TOP_RIGHT = 1
    TOP_LEFT_TO_BOTTOM_RIGHT = 2


def search_horizontally(grid: list[str], word: str) -> int:
    """Count the number of times a word appears in a grid horizontally."""
    count = 0
    for row in grid:
        count += row.count(word)
    return count


def search_vertically(grid: list[str], word: str) -> int:
    """Count the number of times a word appears in a grid vertically."""
    count = 0
    for col in range(len(grid[0])):
        count += "".join([row[col] for row in grid]).count(word)
    return count


def search_diagonally(grid: list[str], direction: Direction, word: str) -> int:
    """Count the number of times a word appears in a grid diagonally. Either from bottom left to top right or top left to bottom right."""

    count = 0
    if direction == Direction.BOTTOM_LEFT_TO_TOP_RIGHT:
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                if i + len(word) <= len(grid) and j + len(word) <= len(grid[0]):
                    if "".join([grid[i + k][j + k] for k in range(len(word))]) == word:
                        count += 1
    else:
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                if i - len(word) >= -1 and j + len(word) <= len(grid[0]):
                    if "".join([grid[i - k][j + k] for k in range(len(word))]) == word:
                        count += 1
    return count


def search_word(grid: list[str], word: str) -> int:
    """Count the number of times a word appears in a grid."""
    sh = search_horizontally(grid, word)
    sv = search_vertically(grid, word)
    sd_bl = search_diagonally(grid, Direction.BOTTOM_LEFT_TO_TOP_RIGHT, word)
    sd_tl = search_diagonally(grid, Direction.TOP_LEFT_TO_BOTTOM_RIGHT, word)

    return sh + sv + sd_bl + sd_tl


with open("input.txt") as f:
    grid = f.read().splitlines()

xmas = search_word(grid, "XMAS")
samx = search_word(grid, "SAMX")

ic(f"XMAS appears {xmas + samx} times in the grid.")
