import sys

lines = sys.stdin.read().split()
n, grid = int(lines[0]), lines[1:]


def encode(row, column, size):
    first = grid[row][column]
    if all(
        grid[r][c] == first
        for r in range(row, row + size)
        for c in range(column, column + size)
    ):
        return first
    half = size // 2
    return (
        "("
        + "".join(
            encode(row + dr, column + dc, half)
            for dr, dc in [(0, 0), (0, half), (half, 0), (half, half)]
        )
        + ")"
    )


print(encode(0, 0, n))
