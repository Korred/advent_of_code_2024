import re
from dataclasses import dataclass
from typing import List, Tuple, TypeAlias

from icecream import ic
from sympy import Symbol, linsolve

# pre-compile regex patterns
x_pattern = re.compile(r"X[\+=]([+-]?\d+)")
y_pattern = re.compile(r"Y[\+=]([+-]?\d+)")

Node: TypeAlias = Tuple[int, int]


@dataclass
class Button:
    x_change: int
    y_change: int
    cost: int


@dataclass
class ClawMachine:
    price_location: Node
    button_a: Button
    button_b: Button

    def solve(self) -> int:
        # Solve the system of equations and return the cost of the solution
        a = Symbol("a", integer=True)
        b = Symbol("b", integer=True)

        eq1 = (
            self.button_a.x_change * a
            + self.button_b.x_change * b
            - self.price_location[0]
        )
        eq2 = (
            self.button_a.y_change * a
            + self.button_b.y_change * b
            - self.price_location[1]
        )

        solution = list(linsolve([eq1, eq2], a, b))[0]
        a_val, b_val = solution

        # We only care about integer solutions
        if all(val.is_integer for val in (a_val, b_val)):
            return self.button_a.cost * a_val + self.button_b.cost * b_val
        else:
            return 0


def parse_coordinates(line: str) -> tuple[int, int]:
    # Extract numbers after X and Y, handling + signs
    x = int(x_pattern.search(line).group(1))
    y = int(y_pattern.search(line).group(1))
    return x, y


def parse_claw_machines_data(input_text: str) -> List[ClawMachine]:
    machines = []
    blocks = input_text.strip().split("\n\n")

    for block in blocks:
        lines = block.split("\n")

        a_x, a_y = parse_coordinates(lines[0])
        b_x, b_y = parse_coordinates(lines[1])
        prize_x, prize_y = parse_coordinates(lines[2])

        # Only thing changed for task 2
        prize_x += 10000000000000
        prize_y += 10000000000000


        machine = ClawMachine(
            price_location=(prize_x, prize_y),
            button_a=Button(x_change=a_x, y_change=a_y, cost=3),
            button_b=Button(x_change=b_x, y_change=b_y, cost=1),
        )
        machines.append(machine)

    return machines


with open("input.txt") as file:
    machines = parse_claw_machines_data(file.read())


total_cost = sum(machine.solve() for machine in machines)
ic(f"Total cost: {total_cost}")
