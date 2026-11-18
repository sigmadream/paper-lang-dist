import sys

def main():
    data = sys.stdin.buffer.readline().strip()
    if not data:
        return

    n = int(data)
    moves = []
    append = moves.append

    append(str((1 << n) - 1) + '\n')

    def hanoi(k, start, mid, end):
        if k == 0:
            return
        hanoi(k - 1, start, end, mid)
        append(f"{start} {end}\n")
        hanoi(k - 1, mid, start, end)

    hanoi(n, 1, 2, 3)
    sys.stdout.write(''.join(moves))

if __name__ == "__main__":
    main()