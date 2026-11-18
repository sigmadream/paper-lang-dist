import sys


def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    n = int(data[0])
    out = [str((1 << n) - 1) + "\n"]

    def hanoi(k, start, mid, end):
        if k == 1:
            out.append(f"{start} {end}\n")
            return

        hanoi(k - 1, start, end, mid)
        out.append(f"{start} {end}\n")
        hanoi(k - 1, mid, start, end)

    hanoi(n, 1, 2, 3)
    sys.stdout.write("".join(out))


if __name__ == "__main__":
    solve()