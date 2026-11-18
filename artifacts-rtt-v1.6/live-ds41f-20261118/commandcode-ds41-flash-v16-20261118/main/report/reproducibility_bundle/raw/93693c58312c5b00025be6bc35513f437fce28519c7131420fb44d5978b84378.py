import sys

def main():
    data = sys.stdin.read().split()
    if len(data) < 2:
        return
    s, t = data[0], data[1]

    count = [0] * 26

    for c in s:
        count[ord(c) - ord('a')] += 1

    for c in t:
        count[ord(c) - ord('a')] -= 1

    for x in count:
        if x != 0:
            print(0)
            return

    print(1)

if __name__ == "__main__":
    main()