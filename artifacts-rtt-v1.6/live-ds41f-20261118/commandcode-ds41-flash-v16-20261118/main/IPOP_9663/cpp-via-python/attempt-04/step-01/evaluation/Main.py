import sys


def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    n = int(data[0])
    full = (1 << n) - 1
    ans = 0

    def solve(row, cols, diag1, diag2):
        nonlocal ans
        if row == n:
            ans += 1
            return

        available = full & ~(cols | diag1 | diag2)
        while available:
            bit = available & -available
            available -= bit
            solve(row + 1, cols | bit, (diag1 | bit) << 1, (diag2 | bit) >> 1)

    solve(0, 0, 0, 0)
    sys.stdout.write(str(ans) + "\n")


if __name__ == "__main__":
    main()