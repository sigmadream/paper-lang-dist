import sys

def main():
    data = sys.stdin.read().split()
    if not data:
        return
    n = int(data[0])
    a = list(map(int, data[1:1+n]))
    best = cur = a[0]
    for i in range(1, n):
        cur = max(a[i], cur + a[i])
        best = max(best, cur)
    print(best)

main()