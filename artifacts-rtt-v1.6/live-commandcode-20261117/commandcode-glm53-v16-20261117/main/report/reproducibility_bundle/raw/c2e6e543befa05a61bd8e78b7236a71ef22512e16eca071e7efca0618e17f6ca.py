import sys

def solve(grid, r, c, size, out):
    first = grid[r][c]
    same = True
    for i in range(r, r + size):
        row = grid[i]
        for j in range(c, c + size):
            if row[j] != first:
                same = False
                break
        if not same:
            break
    if same:
        out.append(first)
        return
    half = size // 2
    out.append('(')
    solve(grid, r, c, half, out)
    solve(grid, r, c + half, out)
    solve(grid, r + half, c, out)
    solve(grid, r + half, c + half, out)
    out.append(')')

def main():
    data = sys.stdin.read().split()
    if not data:
        return
    n = int(data[0])
    grid = data[1:1+n]
    out = []
    solve(grid, 0, 0, n, out)
    print(''.join(out))

main()