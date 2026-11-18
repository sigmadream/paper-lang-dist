import sys

def solve(grid, r, c, size):
    first = grid[r][c]
    for i in range(r, r + size):
        for j in range(c, c + size):
            if grid[i][j] != first:
                half = size // 2
                return (
                    "("
                    + solve(grid, r, c, half)
                    + solve(grid, r, c + half, half)
                    + solve(grid, r + half, c, half)
                    + solve(grid, r + half, c + half, half)
                    + ")"
                )
    return first

def main():
    data = sys.stdin.read().split()
    if not data:
        return
    n = int(data[0])
    grid = data[1:1 + n]
    sys.stdout.write(solve(grid, 0, 0, n) + "\n")

if __name__ == "__main__":
    main()