def solve(r):
    global ans
    if r == n:
        ans += 1
        return
    for c in range(n):
        if col[c] or diag1[r + c] or diag2[r - c + n - 1]:
            continue
        col[c] = diag1[r + c] = diag2[r - c + n - 1] = True
        solve(r + 1)
        col[c] = diag1[r + c] = diag2[r - c + n - 1] = False

n, ans = 0, 0
col, diag1, diag2 = [False] * 15, [False] * 30, [False] * 30

n = int(input())
solve(0)
print(ans)
