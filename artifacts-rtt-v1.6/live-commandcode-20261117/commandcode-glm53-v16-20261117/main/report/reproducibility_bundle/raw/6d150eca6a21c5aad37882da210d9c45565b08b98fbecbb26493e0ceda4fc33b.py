import sys

def main():
    data = sys.stdin.read().split()
    if not data:
        return
    n = int(data[0])
    grid = data[1:1+n]
    out = []

    def solve(r, c, size):
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
        solve(r, c, half)
        solve(r, c + half, half)
        solve(r + half, c, half)
        solve(r + half, c + half, half)
        out.append(')')

    solve(0, 0, n)
    print(''.join(out))

main()