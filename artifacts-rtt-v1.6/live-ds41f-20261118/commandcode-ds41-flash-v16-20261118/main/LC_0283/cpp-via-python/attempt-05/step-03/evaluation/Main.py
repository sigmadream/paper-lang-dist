import sys

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    n = int(data[0])
    a = [int(data[i + 1]) for i in range(n)]

    write = 0
    for read in range(n):
        if a[read] != 0:
            a[write], a[read] = a[read], a[write]
            write += 1

    sys.stdout.write(" ".join(map(str, a)) + "\n")

if __name__ == "__main__":
    main()