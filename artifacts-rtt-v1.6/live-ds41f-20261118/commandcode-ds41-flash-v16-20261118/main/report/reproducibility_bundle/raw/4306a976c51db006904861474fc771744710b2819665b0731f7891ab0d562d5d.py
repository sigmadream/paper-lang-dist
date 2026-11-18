import sys

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    n = int(data[0])
    a = [int(x) for x in data[1:1+n]]
    if n == 0:
        return

    cur = a[0]
    best = a[0]

    for i in range(1, n):
        cur = max(a[i], cur + a[i])
        best = max(best, cur)

    sys.stdout.write(str(best) + '\n')

if __name__ == "__main__":
    main()