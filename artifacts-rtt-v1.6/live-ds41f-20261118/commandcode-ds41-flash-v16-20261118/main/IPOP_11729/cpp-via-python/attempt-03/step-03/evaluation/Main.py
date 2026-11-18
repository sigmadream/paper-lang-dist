import sys

def main():
    data = sys.stdin.read().split()
    if not data:
        return

    n = int(data[0])
    moves = []

    def hanoi(count, start, mid, end):
        if count == 1:
            moves.append(f"{start} {end}\n")
            return
        hanoi(count - 1, start, end, mid)
        moves.append(f"{start} {end}\n")
        hanoi(count - 1, mid, start, end)

    total = (1 << n) - 1
    hanoi(n, 1, 2, 3)

    sys.stdout.write(str(total) + "\n" + "".join(moves))

if __name__ == "__main__":
    main()