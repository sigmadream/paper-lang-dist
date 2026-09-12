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

n = int(input())
ans = 0
col = [False] * n
diag1 = [False] * (2 * n - 1)
diag2 = [False] * (2 * n - 1)
solve(0)
print(ans)
