import sys

def main():
    data = sys.stdin.read().split()
    s, t = data[0], data[1]
    counts = [0] * 26
    for c in s:
        counts[ord(c) - ord('a')] += 1
    for c in t:
        counts[ord(c) - ord('a')] -= 1
    print(1 if all(x == 0 for x in counts) else 0)

main()