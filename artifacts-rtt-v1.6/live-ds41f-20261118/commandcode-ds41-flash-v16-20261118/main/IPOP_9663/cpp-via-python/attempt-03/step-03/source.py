import sys

def main():
    data = sys.stdin.read().strip().split()
    if not data:
        return

    n = int(data[0])
    full = (1 << n) - 1
    answer = 0

    def solve(cols, diag1, diag2):
        nonlocal answer

        if cols == full:
            answer += 1
            return

        available = ~(cols | diag1 | diag2) & full
        while available:
            bit = available & -available
            available -= bit
            solve(cols | bit, (diag1 | bit) << 1, (diag2 | bit) >> 1)

    solve(0, 0, 0)
    print(answer)

if __name__ == "__main__":
    main()