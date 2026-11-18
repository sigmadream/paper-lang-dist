import sys

def solve(r, c, size, grid):
    first = grid[r][c]
    for i in range(r, r + size):
        row = grid[i]
        for j in range(c, c + size):
            if row[j] != first:
                half = size // 2
                return ("(" + solve(r, c, half, grid) + solve(r, c + half, half, grid)
                        + solve(r + half, c, half, grid) + solve(r + half, c + half, half, grid) + ")")
    return first

def main():
    data = sys.stdin.read().split()
    if not data:
        return
    n = int(data[0])
    grid = data[1:1+n]
    print(solve(0, 0, n, grid))

main()