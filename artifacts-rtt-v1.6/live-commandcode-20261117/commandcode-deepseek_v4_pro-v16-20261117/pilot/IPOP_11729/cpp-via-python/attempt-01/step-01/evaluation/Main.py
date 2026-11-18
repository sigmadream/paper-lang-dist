import sys

def hanoi(n, start, mid, end, moves):
    if n == 1:
        moves.append((start, end))
        return
    hanoi(n - 1, start, end, mid, moves)
    moves.append((start, end))
    hanoi(n - 1, mid, start, end, moves)

def main():
    data = sys.stdin.read().strip().split()
    if not data:
        return
    n = int(data[0])
    moves = []
    hanoi(n, 1, 2, 3, moves)
    print(len(moves))
    for a, b in moves:
        print(f"{a} {b}")

if __name__ == "__main__":
    main()