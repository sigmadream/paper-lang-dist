import sys

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    n = int(data[0])
    moves = []

    def hanoi(k, start, mid, end):
        if k == 1:
            moves.append(f"{start} {end}\n")
            return

        hanoi(k - 1, start, end, mid)
        moves.append(f"{start} {end}\n")
        hanoi(k - 1, mid, start, end)

    hanoi(n, 1, 2, 3)

    result = [str((1 << n) - 1) + "\n"]
    result.extend(moves)
    sys.stdout.write("".join(result))

if __name__ == "__main__":
    main()