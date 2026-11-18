import sys


def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    n = int(data[0])
    moves = bytearray()

    def hanoi(k, start, mid, end):
        if k == 1:
            moves.extend((48 + start, 32, 48 + end, 10))
            return

        hanoi(k - 1, start, end, mid)
        moves.extend((48 + start, 32, 48 + end, 10))
        hanoi(k - 1, mid, start, end)

    hanoi(n, 1, 2, 3)

    sys.stdout.buffer.write(str((1 << n) - 1).encode() + b'\n')
    sys.stdout.buffer.write(moves)


if __name__ == "__main__":
    main()