import sys

def main():
    data = sys.stdin.read().split()
    if len(data) < 2:
        return

    s, t = data[0], data[1]

    counts = [0] * 26
    for ch in s:
        counts[ord(ch) - ord('a')] += 1
    for ch in t:
        counts[ord(ch) - ord('a')] -= 1

    valid = all(c == 0 for c in counts)
    print(1 if valid else 0)

if __name__ == "__main__":
    main()