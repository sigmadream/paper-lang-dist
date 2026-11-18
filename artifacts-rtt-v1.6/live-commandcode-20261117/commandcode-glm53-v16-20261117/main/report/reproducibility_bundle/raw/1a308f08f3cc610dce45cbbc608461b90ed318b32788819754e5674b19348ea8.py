import sys

def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    a = [int(x) for x in data[1:1+n]]
    write = 0
    for read in range(n):
        if a[read] != 0:
            a[write], a[read] = a[read], a[write]
            write += 1
    print(" ".join(map(str, a)))

main()