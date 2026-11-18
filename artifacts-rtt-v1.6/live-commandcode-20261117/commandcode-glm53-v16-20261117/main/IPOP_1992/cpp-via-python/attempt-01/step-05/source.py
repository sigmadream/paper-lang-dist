import sys

def solve(grid, r, c, size):
    first = grid[r][c]
    same = True
    for i in range(r, r + size):
        if not same:
            break
        for j in range(c, c + size):
            if grid[i][j] != first:
                same = False
                break
    if same:
        return first
    half = size // 2
    return ("(" + solve(grid, r, c, half)
            + solve(grid, r, c + half, half)
            + solve(grid, r + half, c, half)
            + solve(grid, r + half, c + half, half) + ")")

def main():
    data = sys.stdin.read().split()
    if not data:
        return
    n = int(data[0])
    grid = data[1:1 + n]
    print(solve(grid, 0, 0, n))

main()