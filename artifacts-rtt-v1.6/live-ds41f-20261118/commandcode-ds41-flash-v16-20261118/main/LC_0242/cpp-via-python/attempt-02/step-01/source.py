import sys
from collections import Counter

def main():
    data = sys.stdin.read().split()
    if len(data) < 2:
        return
    s, t = data[0], data[1]
    print(1 if Counter(s) == Counter(t) else 0)

if __name__ == "__main__":
    main()