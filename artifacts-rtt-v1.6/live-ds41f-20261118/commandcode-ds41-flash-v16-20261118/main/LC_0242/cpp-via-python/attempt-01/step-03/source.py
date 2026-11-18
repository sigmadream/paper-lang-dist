import sys

def main():
    data = sys.stdin.read().split()
    s = data[0]
    t = data[1]

    counts = [0] * 26
    for ch in s:
        counts[ord(ch) - ord('a')] += 1
    for ch in t:
        counts[ord(ch) - ord('a')] -= 1

    for x in counts:
        if x != 0:
            print(0)
            return

    print(1)

if __name__ == "__main__":
    main()