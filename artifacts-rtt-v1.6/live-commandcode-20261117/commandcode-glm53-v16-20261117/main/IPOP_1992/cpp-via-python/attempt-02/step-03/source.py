import sys

def solve(r, c, size):
    first = grid[r][c]
    same = all(grid[i][j] == first for i in range(r, r + size) for j in range(c, c + size))
    if same:
        return first
    half = size // 2
    return ("(" + solve(r, c, half) + solve(r, c + half, half)
            + solve(r + half, c, half) + solve(r + half, c + half, half) + ")")

def main():
    data = sys.stdin.read().split()
    if not data:
        return
    global grid
    n = int(data[0])
    grid = data[1:1 + n]
    print(solve(0, 0, n))

main()