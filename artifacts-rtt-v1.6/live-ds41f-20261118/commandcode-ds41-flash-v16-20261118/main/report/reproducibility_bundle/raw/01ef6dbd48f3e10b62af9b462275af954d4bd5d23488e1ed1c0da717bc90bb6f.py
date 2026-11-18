import sys


def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    n = int(data[0])
    full = (1 << n) - 1
    ans = 0

    def solve(cols, diag1, diag2):
        nonlocal ans

        if cols == full:
            ans += 1
            return

        available = ~(cols | diag1 | diag2) & full
        while available:
            bit = available & -available
            available -= bit
            solve(cols | bit, (diag1 | bit) << 1, (diag2 | bit) >> 1)

    solve(0, 0, 0)
    print(ans)


if __name__ == "__main__":
    main()