import sys


def hanoi(n, start, mid, end, moves):
    if n == 1:
        moves.append(f"{start} {end}\n")
        return

    hanoi(n - 1, start, end, mid, moves)
    moves.append(f"{start} {end}\n")
    hanoi(n - 1, mid, start, end, moves)


def main():
    data = sys.stdin.readline()
    if not data:
        return

    n = int(data.strip())
    moves = []
    hanoi(n, 1, 2, 3, moves)

    count = (1 << n) - 1
    sys.stdout.write(str(count) + "\n")
    sys.stdout.write("".join(moves))


if __name__ == "__main__":
    main()