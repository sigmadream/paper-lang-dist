import sys

def main():
    data = sys.stdin.read().split()
    s, t = data[0], data[1]
    counts = [0] * 26
    for ch in s:
        counts[ord(ch) - ord('a')] += 1
    for ch in t:
        counts[ord(ch) - ord('a')] -= 1
    print(1 if all(x == 0 for x in counts) else 0)

if __name__ == "__main__":
    main()