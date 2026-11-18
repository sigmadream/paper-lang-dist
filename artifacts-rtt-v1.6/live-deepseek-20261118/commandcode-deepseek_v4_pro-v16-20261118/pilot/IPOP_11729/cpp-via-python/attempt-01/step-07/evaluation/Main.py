import sys

def hanoi(n, a, b, c):
    if n == 1:
        sys.stdout.write(f"{a} {c}\n")
        return
    hanoi(n - 1, a, c, b)
    sys.stdout.write(f"{a} {c}\n")
    hanoi(n - 1, b, a, c)

def main():
    data = sys.stdin.read().strip().split()
    if not data:
        return
    n = int(data[0])
    sys.stdout.write(str((1 << n) - 1) + "\n")
    hanoi(n, 1, 2, 3)

if __name__ == "__main__":
    main()