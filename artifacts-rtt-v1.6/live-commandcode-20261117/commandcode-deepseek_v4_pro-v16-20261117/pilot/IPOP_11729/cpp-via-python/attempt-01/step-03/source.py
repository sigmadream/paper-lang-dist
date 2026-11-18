import sys

def hanoi(n, start, mid, end, moves):
    if n == 1:
        moves.append(f"{start} {end}")
        return
    hanoi(n - 1, start, end, mid, moves)
    moves.append(f"{start} {end}")
    hanoi(n - 1, mid, start, end, moves)

def main():
    data = sys.stdin.read().split()
    if not data:
        return
    n = int(data[0])
    moves = []
    hanoi(n, 1, 2, 3, moves)

    out = sys.stdout
    out.write(str(len(moves)) + "\n")
    out.write("\n".join(moves))
    out.write("\n")

if __name__ == "__main__":
    main()