import sys

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n = data[0]
    a = data[1:1 + n]

    write = 0
    for read in range(n):
        if a[read] != 0:
            a[write], a[read] = a[read], a[write]
            write += 1

    sys.stdout.write(' '.join(map(str, a)) + '\n')

if __name__ == "__main__":
    main()