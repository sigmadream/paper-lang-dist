import sys

def solve(r, c, sz):
    first = grid[r][c]
    for i in range(r, r + sz):
        for j in range(c, c + sz):
            if grid[i][j] != first:
                h = sz // 2
                return "(" + solve(r, c, h) + solve(r, c + h, h) \
                       + solve(r + h, c, h) + solve(r + h, c + h, h) + ")"
    return first

data = sys.stdin.read().split()
if not data:
    sys.exit(0)
n = int(data[0])
grid = data[1:1 + n]
print(solve(0, 0, n))