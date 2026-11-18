import sys
import math

def main():
    data = sys.stdin.read().split()
    if len(data) < 2:
        return
    a, b = int(data[0]), int(data[1])
    g = math.gcd(a, b)
    print(g)
    print((a // g) * b)

if __name__ == "__main__":
    main()