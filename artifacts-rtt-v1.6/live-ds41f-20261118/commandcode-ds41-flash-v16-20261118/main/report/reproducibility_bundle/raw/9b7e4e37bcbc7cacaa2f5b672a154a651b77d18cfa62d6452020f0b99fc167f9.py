import sys


def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    n = int(data[0])
    full = (1 << n) - 1
    ans = 0

    def dfs(cols, diag1, diag2):
        nonlocal ans
        if cols == full:
            ans += 1
            return

        avail = full & ~(cols | diag1 | diag2)
        while avail:
            bit = avail & -avail
            avail -= bit
            dfs(cols | bit, ((diag1 | bit) << 1) & full, (diag2 | bit) >> 1)

    dfs(0, 0, 0)
    sys.stdout.write(str(ans) + "\n")


if __name__ == "__main__":
    main()