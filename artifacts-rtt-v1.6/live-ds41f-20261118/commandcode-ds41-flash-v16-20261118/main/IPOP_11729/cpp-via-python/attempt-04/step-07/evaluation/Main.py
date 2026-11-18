import sys


def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    n = int(data[0])
    moves = []

    def hanoi(k, start, mid, end):
        if k == 1:
            moves.append(f"{start} {end}")
            return
        hanoi(k - 1, start, end, mid)
        moves.append(f"{start} {end}")
        hanoi(k - 1, mid, start, end)

    count = (1 << n) - 1
    hanoi(n, 1, 2, 3)

    sys.stdout.write(str(count) + "\n")
    if moves:
        sys.stdout.write("\n".join(moves) + "\n")


if __name__ == "__main__":
    main()