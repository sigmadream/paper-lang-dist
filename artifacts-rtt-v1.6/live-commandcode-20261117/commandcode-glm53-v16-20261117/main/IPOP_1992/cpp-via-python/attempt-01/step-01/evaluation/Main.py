import sys

def solve(grid, r, c, size):
    first = grid[r][c]
    if all(grid[i][j] == first for i in range(r, r + size) for j in range(c, c + size)):
        return first
    half = size // 2
    tl = solve(grid, r, c, half)
    tr = solve(grid, r, c + half, half)
    bl = solve(grid, r + half, c, half)
    br = solve(grid, r + half, c + half, half)
    return "(" + tl + tr + bl + br + ")"

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    n = int(tokens[0])
    grid = tokens[1:1 + n]
    print(solve(grid, 0, 0, n))

main()