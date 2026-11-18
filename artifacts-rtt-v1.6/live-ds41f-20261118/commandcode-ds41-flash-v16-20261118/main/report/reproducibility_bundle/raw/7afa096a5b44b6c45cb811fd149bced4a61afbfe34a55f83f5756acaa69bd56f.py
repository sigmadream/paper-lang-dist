import sys

def main():
    data = sys.stdin.read().split()
    if not data:
        return

    n = int(data[0])
    a = list(map(int, data[1:1 + n]))

    write = 0
    for read in range(n):
        if a[read] != 0:
            a[write], a[read] = a[read], a[write]
            write += 1

    print(" ".join(map(str, a)))

if __name__ == "__main__":
    main()