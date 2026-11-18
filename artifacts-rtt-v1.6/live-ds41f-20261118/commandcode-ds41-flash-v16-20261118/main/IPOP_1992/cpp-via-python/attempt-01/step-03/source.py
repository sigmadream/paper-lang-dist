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
        return (
            "("
            + solve(r, c, half)
            + solve(r, c + half, half)
            + solve(r + half, c, half)
            + solve(r + half, c + half, half)
            + ")"
        )

    print(solve(0, 0, n))

if __name__ == "__main__":
    main()