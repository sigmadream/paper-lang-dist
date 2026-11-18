import sys


def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    n = int(data[0])
    moves = []
    append = moves.append

    def hanoi(k, start, mid, end):
        if k == 1:
            append(f"{start} {end}")
            return
        hanoi(k - 1, start, end, mid)
        append(f"{start} {end}")
        hanoi(k - 1, mid, start, end)

    hanoi(n, 1, 2, 3)

    output = [str(len(moves)), "\n", "\n".join(moves), "\n"]
    sys.stdout.write("".join(output))


if __name__ == "__main__":
    main()