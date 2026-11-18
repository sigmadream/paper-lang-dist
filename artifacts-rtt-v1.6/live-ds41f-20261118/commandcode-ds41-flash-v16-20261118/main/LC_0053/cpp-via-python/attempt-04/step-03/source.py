import sys

def main() -> None:
    tokens = sys.stdin.buffer.read().split()
    if not tokens:
        return

    n = int(tokens[0])
    a = [int(x) for x in tokens[1:1 + n]]

    cur = best = a[0]
    for x in a[1:]:
        cur = max(x, cur + x)
        best = max(best, cur)

    print(best)

if __name__ == "__main__":
    main()