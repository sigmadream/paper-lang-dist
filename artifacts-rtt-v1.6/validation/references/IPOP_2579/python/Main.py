import sys

n, *scores = map(int, sys.stdin.buffer.read().split())
scores = [0] + scores
best = [0] * (n + 1)
if n >= 1:
    best[1] = scores[1]
if n >= 2:
    best[2] = scores[1] + scores[2]
for step in range(3, n + 1):
    best[step] = max(best[step - 2], best[step - 3] + scores[step - 1]) + scores[step]
print(best[n])
