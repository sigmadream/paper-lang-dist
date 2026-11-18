import sys

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    n = int(data[0])

    moves = [(1 << n) - 1]

    def hanoi(k, start, mid, end):
        if k == 0:
            return
        if k == 1:
            moves.append(f"{start} {end}")
            return

        hanoi(k - 1, start, end, mid)
        moves.append(f"{start} {end}")
        hanoi(k - 1, mid, start, end)

    hanoi(n, 1, 2, 3)

    sys.stdout.write("\n".join(map(str, moves)) + "\n")

if __name__ == "__main__":
    main()