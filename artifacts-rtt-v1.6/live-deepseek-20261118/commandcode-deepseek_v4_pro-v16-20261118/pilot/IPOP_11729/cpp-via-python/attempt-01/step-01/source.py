import sys

def main():
    data = sys.stdin.read().strip().split()
    if not data:
        return

    n = int(data[0])
    print((1 << n) - 1)

    def hanoi(count, start, mid, end):
        if count == 1:
            sys.stdout.write(f"{start} {end}\n")
            return
        hanoi(count - 1, start, end, mid)
        sys.stdout.write(f"{start} {end}\n")
        hanoi(count - 1, mid, start, end)

    hanoi(n, 1, 2, 3)

if __name__ == "__main__":
    main()