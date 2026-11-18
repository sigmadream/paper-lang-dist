import sys

def hanoi(n, start, mid, end, moves):
    if n == 1:
        moves.append(f"{start} {end}")
        return
    hanoi(n - 1, start, end, mid, moves)
    moves.append(f"{start} {end}")
    hanoi(n - 1, mid, start, end, moves)

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    n = int(data[0])
    moves = []
    hanoi(n, 1, 2, 3, moves)

    out = [str(len(moves))]
    out.extend(moves)
    sys.stdout.write("\n".join(out) + "\n")

if __name__ == "__main__":
    main()