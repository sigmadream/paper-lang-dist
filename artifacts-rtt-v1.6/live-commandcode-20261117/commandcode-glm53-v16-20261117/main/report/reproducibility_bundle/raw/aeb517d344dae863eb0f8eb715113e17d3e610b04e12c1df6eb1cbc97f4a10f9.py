import sys

n = int(sys.stdin.read())
counts = [0] * (n + 1)
for number in range(1, n + 1):
    counts[number] = counts[number >> 1] + (number & 1)
print(*counts)
