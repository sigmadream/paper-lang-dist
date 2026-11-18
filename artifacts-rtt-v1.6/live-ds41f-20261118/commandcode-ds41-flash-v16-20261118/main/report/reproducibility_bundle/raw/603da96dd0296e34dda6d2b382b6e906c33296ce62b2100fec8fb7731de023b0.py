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

    if any(x != 0 for x in counts):
        print(0)
    else:
        print(1)

if __name__ == "__main__":
    main()