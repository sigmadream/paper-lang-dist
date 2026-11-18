import sys

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return
    n = data[0]
    a = data[1:1 + n]
    cur = a[0]
    best = a[0]
    for i in range(1, n):
        cur = max(a[i], cur + a[i])
        best = max(best, cur)
    print(best)

if __name__ == "__main__":
    main()