import re
from collections import defaultdict
from dataclasses import dataclass
from math import prod
from typing import DefaultDict, List, Tuple

from icecream import ic

# Constants
WIDTH = 101
HEIGHT = 103
SIMULATION_STEPS = 100


@dataclass
class Robot:
    position: Tuple[int, int]
    velocity: Tuple[int, int]

    def move(self, limits: Tuple[int, int] = (WIDTH, HEIGHT)) -> Tuple[int, int]:
        """Move robot according to velocity and wrap around limits."""
        x, y = self.position
        dx, dy = self.velocity
        self.position = ((x + dx) % limits[0], (y + dy) % limits[1])
        return self.position


def parse_coordinates(input_str: str) -> Tuple[Tuple[int, int], Tuple[int, int]]:
    pattern = r"-?\d+"

    numbers = [int(x) for x in re.findall(pattern, input_str)]
    position = (numbers[0], numbers[1])
    velocity = (numbers[2], numbers[3])

    return position, velocity


def count_robots_in_quadrants(
    width: int, height: int, robot_positions: DefaultDict[Tuple[int, int], List[Robot]]
) -> List[int]:
    """Count robots in each quadrant of the grid."""
    quadrants = [0] * 4
    middle_x = width // 2
    middle_y = height // 2

    quadrant_limits = [
        (0, middle_x, 0, middle_y),  # top left
        (middle_x + 1, width, 0, middle_y),  # top right
        (0, middle_x, middle_y + 1, height),  # bottom left
        (middle_x + 1, width, middle_y + 1, height),  # bottom right
    ]

    for position, robots in robot_positions.items():
        x, y = position
        for q, (x_min, x_max, y_min, y_max) in enumerate(quadrant_limits):
            if x_min <= x < x_max and y_min <= y < y_max:
                quadrants[q] += len(robots)
                break

    return quadrants


def load_data(file_path: str) -> DefaultDict[Tuple[int, int], List[Robot]]:
    robot_positions: DefaultDict[Tuple[int, int], List[Robot]] = defaultdict(list)

    with open(file_path) as file:
        lines = file.readlines()
        for line in lines:
            position, velocity = parse_coordinates(line)
            robot_positions[position].append(Robot(position, velocity))

    return robot_positions


def draw_robots(width: int, height: int, robot_positions: DefaultDict[Tuple[int, int], List[Robot]]) -> None:
    grid = [[' ' for _ in range(width)] for _ in range(height)]
    for position in robot_positions.keys():
        x, y = position
        grid[y][x] = '#'

    print("\n".join("".join(row) for row in grid))


robot_positions = load_data("input.txt")

# How was this solved?
#
# I printed the grid of robots at different seconds and looked for something that looked like a pattern.
# At second 76 I noticed a two very distinct but broken up horizontal lines.
# Those horizontal lines were repeating/oscillating every 103 seconds. So instead of analyzing all the seconds I just
# printed the grid at second 76 and then at second 76 + 103, 76 + 103 + 103, 76 + 103 + 103 + 103, etc.
# This ultimately led me to the solution - the tree is shown below.


# Interesting pattern at second 76
output_s = 76
for s in range(1, 8000):
    new_positions = defaultdict(list)
    for robots in robot_positions.values():
        for robot in robots:
            robot.move()

            new_positions[robot.position].append(robot)
    robot_positions = new_positions

    if s == output_s:
        ic(f"Second: {s}")
        draw_robots(WIDTH, HEIGHT, robot_positions)
        input("Press Enter to continue...")
        print()
        output_s += 103


""""
                 ###############################                            #
               # #                             #                                  #
                 #                             #                                          #
                 #                             #                            #
                 #                             #
                 #              #              #
                 #             ###             #                        #  #
                 #            #####            #
                 #           #######           #
                 #          #########          #              ##                    #
                 #            #####            #                                   #
                 #           #######           #                     #
                 #          #########          #
                 #         ###########         #                    #               #
                 #        #############        #                              #
                 #          #########          #
     #           #         ###########         #                             #
                 #        #############        #
                 #       ###############       #
          #      #      #################      #                                    #
                 #        #############        #
       #         #       ###############       #             #           #
                 #      #################      #          #
                 #     ###################     #
                 #    #####################    #
                 #             ###             #                                #    #
  #         #    #             ###             #         #             #
                 #             ###             #                        #                      #
                 #                             #                                      #
                 #                             #  # #                        #     #
                 #                             #                                                 # #
                 #                             #
                 ###############################
"""
