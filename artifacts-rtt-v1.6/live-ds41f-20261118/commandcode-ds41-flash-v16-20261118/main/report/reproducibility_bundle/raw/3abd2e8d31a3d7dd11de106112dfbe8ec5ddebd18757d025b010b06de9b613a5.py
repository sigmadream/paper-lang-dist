import sys

m, n = map(int, sys.stdin.buffer.read().split())
row = [1] * n
for _ in range(m - 1):
    for column in range(1, n):
        row[column] += row[column - 1]
print(row[-1])
