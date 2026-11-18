import sys

def solve():
    line = sys.stdin.buffer.readline()
    if not line:
        return

    n = int(line)
    write = sys.stdout.write
    write(str((1 << n) - 1) + "\n")

    buffer = []
    limit = 10000

    def emit(a, b):
        buffer.append(f"{a} {b}\n")
        if len(buffer) >= limit:
            write("".join(buffer))
            buffer.clear()

    def hanoi(k, start, mid, end):
        if k == 1:
            emit(start, end)
            return
        hanoi(k - 1, start, end, mid)
        emit(start, end)
        hanoi(k - 1, mid, start, end)

    hanoi(n, 1, 2, 3)

    if buffer:
        write("".join(buffer))

if __name__ == "__main__":
    solve()