import sys

def hanoi(count, start, via, end, moves):
    if count == 1:
        moves.append(f"{start} {end}")
        return

    hanoi(count - 1, start, end, via, moves)
    moves.append(f"{start} {end}")
    hanoi(count - 1, via, start, end, moves)

def main():
    data = sys.stdin.read().strip().split()
    if not data:
        return

    n = int(data[0])
    moves = []
    hanoi(n, 1, 2, 3, moves)

    output = [str((1 << n) - 1)]
    output.extend(moves)
    sys.stdout.write("\n".join(output) + "\n")

if __name__ == "__main__":
    main()