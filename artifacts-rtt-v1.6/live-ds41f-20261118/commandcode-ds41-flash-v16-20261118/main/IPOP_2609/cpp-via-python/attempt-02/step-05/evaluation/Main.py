import sys
import math

data = list(map(int, sys.stdin.read().split()))

if len(data) < 2:
    sys.exit(0)

a = data[0]
b = data[1]
g = math.gcd(a, b)

print(g)
print((a // g) * b)