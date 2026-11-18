import sys

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return
    n = data[0]
    a = data[1:1 + n]

    cur = a[0]
    best = a[0]

    for x in a[1:]:
        cur = max(x, cur + x)
        best = max(best, cur)

    print(best)

if __name__ == "__main__":
    main()