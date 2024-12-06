from copy import deepcopy
from dataclasses import dataclass
from enum import Enum

from icecream import ic


class Direction(Enum):
    UP = "^"
    DOWN = "v"
    LEFT = "<"
    RIGHT = ">"


class GuardPatrolLoopException(Exception):
    def __init__(self, position: tuple[int, int], direction: Direction):
        self.position = position
        self.direction = direction
        message = (
            f"Guard is stuck in a loop at position {position} facing {direction.value}"
        )
        super().__init__(message)


@dataclass(frozen=True)
class Position:
    x: int
    y: int

    def to_tuple(self) -> tuple[int, int]:
        return (self.x, self.y)

    def next_position(self, direction: Direction) -> "Position":
        match direction:
            case Direction.UP:
                return Position(self.x, self.y - 1)
            case Direction.DOWN:
                return Position(self.x, self.y + 1)
            case Direction.LEFT:
                return Position(self.x - 1, self.y)
            case Direction.RIGHT:
                return Position(self.x + 1, self.y)

    def is_within_bounds(self, width: int, height: int) -> bool:
        return 0 <= self.x < width and 0 <= self.y < height

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"


@dataclass
class Guard:
    position: Position
    direction: Direction

    def turn_right(self) -> "Guard":
        match self.direction:
            case Direction.UP:
                self.direction = Direction.RIGHT
            case Direction.RIGHT:
                self.direction = Direction.DOWN
            case Direction.DOWN:
                self.direction = Direction.LEFT
            case Direction.LEFT:
                self.direction = Direction.UP
        return self

    def move(self, new_position: Position) -> "Guard":
        self.position = new_position
        return self


class GuardMap:
    def __init__(self, data: str):
        self.map, self.guard, self.obstacles = self._process_map(data)
        self.width = len(self.map[0]) if self.map else 0
        self.height = len(self.map)

        self.initial_map = deepcopy(self.map)
        self.initial_obstacles = deepcopy(self.obstacles)

    def _process_map(
        self, data: str
    ) -> tuple[list[list[str]], Guard, set[tuple[int, int]]]:
        processed_map = []
        obstacles = set()
        guard = None
        guard_symbols = {d.value: d for d in Direction}

        for y, line in enumerate(data.strip().split("\n")):
            if not line.strip():
                continue

            row = list(line.strip())
            processed_map.append(row)

            for x, cell in enumerate(row):
                if cell in guard_symbols:
                    guard = Guard(
                        position=Position(x, y), direction=guard_symbols[cell]
                    )
                elif cell == "#":
                    obstacles.add((x, y))

        if guard is None:
            raise ValueError("No guard position (^,v,<,>) found in map")

        return processed_map, guard, obstacles

    def sim_guard_patrol(self):
        # Simulate guard patrol on a copy of the initial guard
        sim_guard = Guard(
            Position(*self.guard.position.to_tuple()), self.guard.direction
        )
        guard_positions = set()

        while sim_guard.position.is_within_bounds(self.width, self.height):
            if (sim_guard.direction, sim_guard.position.to_tuple()) in guard_positions:
                raise GuardPatrolLoopException(
                    sim_guard.position.to_tuple(), sim_guard.direction
                )

            guard_positions.add((sim_guard.direction, sim_guard.position.to_tuple()))

            # Check if there is an obstacle on the next position
            next_pos = sim_guard.position.next_position(sim_guard.direction)
            if next_pos.to_tuple() in self.obstacles:
                sim_guard.turn_right()
                continue

            sim_guard.move(next_pos)

        return {pos for _, pos in guard_positions}

    def add_obstacle(self, position: tuple[int, int]) -> None:
        self.obstacles.add(position)
        self.map[position[1]][position[0]] = "#"

    def reset(self):
        self.map = deepcopy(self.initial_map)
        self.obstacles = deepcopy(self.initial_obstacles)

    def __str__(self) -> str:
        return (
            f"GuardMap({self.width}x{self.height}, "
            f"guard={self.guard}, "
            f"obstacles={len(self.obstacles)})"
        )


with open("input.txt", "r") as f:
    data = f.read()

guard_map = GuardMap(data)
ic(str(guard_map))

# Get initial guard patrol route positions (guaranteed to not contain a loop)
guard_positions = guard_map.sim_guard_patrol()

# Add obstacles on the guard patrol route until a loop is created/detected
loops_detected = 0
for pos in guard_positions:
    # Ignore guard starting position
    if pos == guard_map.guard.position.to_tuple():
        continue

    guard_map.add_obstacle(pos)

    try:
        guard_map.sim_guard_patrol()
    except GuardPatrolLoopException:
        loops_detected += 1

    guard_map.reset()

ic(f"Total loops detected: {loops_detected}")
