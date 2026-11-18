import sys

n, *values = map(int, sys.stdin.buffer.read().split())
nonzero = [value for value in values if value != 0]
print(*(nonzero + [0] * (n - len(nonzero))))
