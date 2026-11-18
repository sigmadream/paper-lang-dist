import sys

def solve(grid, r, c, size):
    first = grid[r][c]
    for i in range(r, r + size):
        for j in range(c, c + size):
            if grid[i][j] != first:
                half = size // 2
                tl = solve(grid, r, c, half)
                tr = solve(grid, r, c + half, half)
                bl = solve(grid, r + half, c, half)
                br = solve(grid, r + half, c + half, half)
                return "(" + tl + tr + bl + br + ")"
    return first

def main():
    data = sys.stdin.read().split()
    if not data:
        return
    n = int(data[0])
    grid = data[1:1 + n]
    print(solve(grid, 0, 0, n))

main()