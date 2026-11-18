import sys

def hanoi(k, start, mid, end, out):
    if k == 1:
        out.append(f"{start} {end}\n")
        return

    hanoi(k - 1, start, end, mid, out)
    out.append(f"{start} {end}\n")
    hanoi(k - 1, mid, start, end, out)

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    n = int(data[0])
    out = [f"{(1 << n) - 1}\n"]

    hanoi(n, 1, 2, 3, out)

    sys.stdout.write("".join(out))

if __name__ == "__main__":
    main()