import sys

def main():
    data = sys.stdin.read().split()
    if not data:
        return

    n = int(data[0])
    a = [int(x) for x in data[1:n + 1]]

    write = 0
    sz = len(a)

    for read in range(min(n, sz)):
        if a[read] != 0:
            a[write], a[read] = a[read], a[write]
            write += 1

    sys.stdout.write(' '.join(map(str, a)) + '\n')

if __name__ == "__main__":
    main()