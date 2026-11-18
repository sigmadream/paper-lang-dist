import sys

def hanoi(count, start, mid, end, out):
    if count == 1:
        out.write(f"{start} {end}\n")
        return
    hanoi(count - 1, start, end, mid, out)
    out.write(f"{start} {end}\n")
    hanoi(count - 1, mid, start, end, out)

def main():
    data = sys.stdin.read().split()
    if not data:
        return
    n = int(data[0])
    out = sys.stdout
    out.write(str((1 << n) - 1) + "\n")
    hanoi(n, 1, 2, 3, out)

if __name__ == "__main__":
    main()