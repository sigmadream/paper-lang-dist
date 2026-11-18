import sys
from collections import Counter

def main():
    data = sys.stdin.read().split()
    s, t = data[0], data[1]
    print(1 if Counter(s) == Counter(t) else 0)

main()