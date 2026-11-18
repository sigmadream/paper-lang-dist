import sys
import io


def hanoi(n, start, mid, end, out):
    if n == 1:
        out.write(f"{start} {end}\n")
        return
    hanoi(n - 1, start, end, mid, out)
    out.write(f"{start} {end}\n")
    hanoi(n - 1, mid, start, end, out)


def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    n = int(data[0])

    moves = io.StringIO()
    hanoi(n, 1, 2, 3, moves)

    result = io.StringIO()
    result.write(str((1 << n) - 1) + "\n")
    result.write(moves.getvalue())

    sys.stdout.write(result.getvalue())


if __name__ == "__main__":
    main()