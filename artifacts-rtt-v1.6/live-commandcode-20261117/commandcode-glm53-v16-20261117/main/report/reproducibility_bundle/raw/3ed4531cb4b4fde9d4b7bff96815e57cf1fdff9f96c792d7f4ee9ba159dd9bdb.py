import sys
from math import gcd

def main():
    data = sys.stdin.read().split()
    if len(data) < 2:
        return
    a, b = int(data[0]), int(data[1])
    g = gcd(a, b)
    print(g)
    print((a // g) * b)

main()