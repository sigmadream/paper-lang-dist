import sys

def solve(r, c, size):
    first = grid[r][c]
    for i in range(r, r + size):
        for j in range(c, c + size):
            if grid[i][j] != first:
                half = size // 2
                return "(" + solve(r, c, half) + solve(r, c + half, half) \
                       + solve(r + half, c, half) + solve(r + half, c + half, half) + ")"
    return first

def main():
    global grid
    data = sys.stdin.read().split()
    if not data:
        return
    n = int(data[0])
    grid = data[1:1 + n]
    print(solve(0, 0, n))

main()