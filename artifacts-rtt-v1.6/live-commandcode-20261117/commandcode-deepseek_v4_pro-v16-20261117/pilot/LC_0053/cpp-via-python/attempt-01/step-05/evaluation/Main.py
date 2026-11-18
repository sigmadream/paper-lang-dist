import sys

def main():
    data = sys.stdin.read().strip().split()
    if not data:
        return
    n = int(data[0])
    if n == 0:
        return
    x = int(data[1])
    cur = x
    best = x
    idx = 2
    for _ in range(1, n):
        x = int(data[idx])
        idx += 1
        cur = max(x, cur + x)
        best = max(best, cur)
    print(best)

if __name__ == "__main__":
    main()