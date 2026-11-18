import sys

def hanoi(k, start, mid, end):
    if k == 1:
        sys.stdout.write(f"{start} {end}\n")
        return
    hanoi(k - 1, start, end, mid)
    sys.stdout.write(f"{start} {end}\n")
    hanoi(k - 1, mid, start, end)

def main():
    data = sys.stdin.read().strip()
    if not data:
        return

    n = int(data)
    sys.stdout.write(f"{(1 << n) - 1}\n")
    hanoi(n, 1, 2, 3)

if __name__ == "__main__":
    main()