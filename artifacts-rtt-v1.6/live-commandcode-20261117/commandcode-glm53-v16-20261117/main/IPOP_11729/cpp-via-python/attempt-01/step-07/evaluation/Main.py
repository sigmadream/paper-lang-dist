import sys

def hanoi(n, start, mid, end, out):
    if n == 1:
        out.append(f"{start} {end}")
        return
    hanoi(n - 1, start, end, mid, out)
    out.append(f"{start} {end}")
    hanoi(n - 1, mid, start, end, out)

def main():
    data = sys.stdin.read().split()
    if not data:
        return
    n = int(data[0])
    out = [str((1 << n) - 1)]
    hanoi(n, 1, 2, 3, out)
    sys.stdout.write("\n".join(out) + "\n")

main()