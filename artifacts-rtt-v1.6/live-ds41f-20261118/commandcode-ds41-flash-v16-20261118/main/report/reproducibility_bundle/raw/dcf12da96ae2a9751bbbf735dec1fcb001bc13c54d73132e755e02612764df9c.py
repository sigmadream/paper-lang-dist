import sys
import math

def main():
    data = sys.stdin.read().split()
    if not data:
        return
    m, n = map(int, data[:2])
    print(math.comb(m + n - 2, m - 1))

if __name__ == "__main__":
    main()