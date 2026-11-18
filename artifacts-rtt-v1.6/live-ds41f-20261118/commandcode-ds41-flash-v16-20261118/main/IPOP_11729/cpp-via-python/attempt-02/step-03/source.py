import sys

def main():
    data = sys.stdin.buffer.readline()
    if not data:
        return

    n = int(data)
    moves = []

    def hanoi(k, start, mid, end):
        if k == 1:
            moves.append(f"{start} {end}\n")
            return
        hanoi(k - 1, start, end, mid)
        moves.append(f"{start} {end}\n")
        hanoi(k - 1, mid, start, end)

    moves.append(str((1 << n) - 1) + "\n")
    hanoi(n, 1, 2, 3)
    sys.stdout.write("".join(moves))

if __name__ == "__main__":
    main()