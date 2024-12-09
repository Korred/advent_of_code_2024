from icecream import ic


def decompress(disk_map: str) -> list[tuple[int, int]]:
    return [(i // 2 if i % 2 == 0 else -1, int(d)) for i, d in enumerate(disk_map)]


def compact(decompressed_map: list[tuple[int, int]]) -> None:
    """Compact the decompressed map in place."""
    for i in range(len(decompressed_map))[::-1]:
        for j in range(i):
            i_val, i_size = decompressed_map[i]
            j_val, j_size = decompressed_map[j]

            if i_val > 0 and j_val < 0 and i_size <= j_size:
                decompressed_map[i] = (-1, i_size)
                decompressed_map[j] = (-1, j_size - i_size)
                decompressed_map.insert(j, (i_val, i_size))
                break


def expand(decompressed_map: list[tuple[int, int]]) -> list[int]:
    return [val for val, size in decompressed_map for _ in range(size)]


def check_sum(expanded_map: list[int]) -> int:
    return sum(i * c for i, c in enumerate(expanded_map) if c >= 0)


with open("input.txt") as f:
    disk_map = f.read()


decompressed = decompress(disk_map)
compact(decompressed)
ic(check_sum(expand(decompressed)))
