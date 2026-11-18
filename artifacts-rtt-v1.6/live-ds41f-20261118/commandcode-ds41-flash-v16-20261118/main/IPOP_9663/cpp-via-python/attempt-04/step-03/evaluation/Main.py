import sys

n = int(sys.stdin.readline())
full_mask = (1 << n) - 1
answer = 0

def solve(row, cols, diag1, diag2):
    global answer
    if row == n:
        answer += 1
        return

    available = full_mask & ~(cols | diag1 | diag2)

    while available:
        bit = available & -available
        available -= bit
        solve(row + 1, cols | bit, (diag1 | bit) << 1, (diag2 | bit) >> 1)

solve(0, 0, 0, 0)
print(answer)