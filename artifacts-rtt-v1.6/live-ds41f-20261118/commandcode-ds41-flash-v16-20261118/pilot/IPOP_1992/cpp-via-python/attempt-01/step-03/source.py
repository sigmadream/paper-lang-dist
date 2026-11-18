import sys


def main():
    data = sys.stdin.read().split()
    if not data:
        return

    n = int(data[0])
    grid = data[1:1 + n]

    def solve(r, c, size):
        first = grid[r][c]
        same = True

        for i in range(r, r + size):
            for j in range(c, c + size):
                if grid[i][j] != first:
                    same = False
                    break
            if not same:
                break

        if same:
            return first

        half = size // 2
        tl = solve(r, c, half)
        tr = solve(r, c + half, half)
        bl = solve(r + half, c, half)
        br = solve(r + half, c + half, half)

        return "(" + tl + tr + bl + br + ")"

    sys.stdout.write(solve(0, 0, n) + "\n")


if __name__ == "__main__":
    main()