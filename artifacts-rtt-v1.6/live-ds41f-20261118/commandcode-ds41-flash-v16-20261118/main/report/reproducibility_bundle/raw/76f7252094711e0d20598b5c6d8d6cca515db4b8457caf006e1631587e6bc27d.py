import sys


def hanoi(k, start, mid, end, out):
    if k == 0:
        return
    if k == 1:
        out.append(f"{start} {end}")
        return

    hanoi(k - 1, start, end, mid, out)
    out.append(f"{start} {end}")
    hanoi(k - 1, mid, start, end, out)


def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    n = int(data[0])
    moves = (1 << n) - 1

    out = [str(moves)]
    hanoi(n, 1, 2, 3, out)

    sys.stdout.write("\n".join(out) + "\n")


if __name__ == "__main__":
    main()