import sys

def main():
    data = sys.stdin.read().split()
    a = list(map(int, data[1:1 + int(data[0])]))
    cur = best = a[0]
    for x in a[1:]:
        cur = max(x, cur + x)
        best = max(best, cur)
    print(best)

main()