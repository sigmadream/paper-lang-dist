import sys

n, first, *values = map(int, sys.stdin.buffer.read().split())
ending = best = first
for value in values:
    ending = max(value, ending + value)
    best = max(best, ending)
print(best)
