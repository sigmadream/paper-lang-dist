import sys
from math import gcd

def main():
    data = sys.stdin.read().split()
    if len(data) < 2:
        return
    a, b = int(data[0]), int(data[1])
    g = gcd(a, b)
    l = (a // g) * b
    print(g)
    print(l)

if __name__ == "__main__":
    main()