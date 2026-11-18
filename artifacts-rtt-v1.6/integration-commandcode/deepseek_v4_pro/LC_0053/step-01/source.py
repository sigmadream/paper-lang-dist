import sys

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    n = int(tokens[0])
    a = list(map(int, tokens[1:1+n]))
    cur = best = a[0]
    for i in range(1, n):
        cur = max(a[i], cur + a[i])
        best = max(best, cur)
    print(best)

if __name__ == "__main__":
    main()