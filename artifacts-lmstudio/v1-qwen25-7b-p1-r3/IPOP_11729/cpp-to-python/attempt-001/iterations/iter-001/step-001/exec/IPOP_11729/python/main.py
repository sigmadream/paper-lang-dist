def hanoi(n, start, mid, end, moves):
    if n == 1:
        moves.append((start, end))
        return
    hanoi(n - 1, start, end, mid, moves)
    moves.append((start, end))
    hanoi(n - 1, mid, start, end, moves)

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    n = int(data[0])
    moves = []
    hanoi(n, 1, 2, 3, moves)
    print(len(moves))
    for move in moves:
        print(move[0], move[1])

if __name__ == "__main__":
    main()
