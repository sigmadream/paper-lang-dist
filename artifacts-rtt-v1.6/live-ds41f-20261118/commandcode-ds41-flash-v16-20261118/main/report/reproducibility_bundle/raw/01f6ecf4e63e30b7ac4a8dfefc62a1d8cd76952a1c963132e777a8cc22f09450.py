import sys

def main():
    data = sys.stdin.readline().strip()
    if not data:
        return
    n = int(data)

    ans = 0
    col = [False] * n
    diag1 = [False] * (2 * n - 1)
    diag2 = [False] * (2 * n - 1)

    def solve(r):
        nonlocal ans
        if r == n:
            ans += 1
            return

        for c in range(n):
            d1 = r + c
            d2 = r - c + n - 1
            if col[c] or diag1[d1] or diag2[d2]:
                continue

            col[c] = diag1[d1] = diag2[d2] = True
            solve(r + 1)
            col[c] = diag1[d1] = diag2[d2] = False

    solve(0)
    print(ans)

if __name__ == "__main__":
    main()