from icecream import ic


def decompress(disk_map: str) -> list[tuple[int, int]]:
    return [
        (i // 2 if i % 2 == 0 else -1, 1)
        for i, d in enumerate(disk_map)
        for _ in range(int(d))
    ]


def compact(decompressed_map: list[tuple[int, int]]) -> None:
    """Compact the decompressed map in place."""
    left, right = 0, len(decompressed_map) - 1

    while left < right:
        while left < right and decompressed_map[left][0] >= 0:
            left += 1
        while left < right and decompressed_map[right][0] == -1:
            right -= 1

        if left < right:
            decompressed_map[left], decompressed_map[right] = (
                decompressed_map[right],
                decompressed_map[left],
            )
            left += 1
            right -= 1


def expand(decompressed_map: list[tuple[int, int]]) -> list[int]:
    return [val for val, size in decompressed_map for _ in range(size)]


def check_sum(expanded_map: list[int]) -> int:
    return sum(i * c for i, c in enumerate(expanded_map) if c >= 0)


with open("input.txt") as f:
    disk_map = f.read()


decompressed = decompress(disk_map)
compact(decompressed)
ic(check_sum(expand(decompressed)))
