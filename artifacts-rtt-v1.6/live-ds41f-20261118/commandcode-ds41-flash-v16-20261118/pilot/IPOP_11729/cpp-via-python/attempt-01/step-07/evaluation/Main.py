import sys

def main() -> None:
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    n = int(data[0])
    count = (1 << n) - 1

    output = bytearray()
    output.extend(str(count).encode())
    output.append(10)

    def hanoi(k: int, start: int, mid: int, end: int) -> None:
        if k == 0:
            return

        hanoi(k - 1, start, end, mid)
        output.append(48 + start)
        output.append(32)
        output.append(48 + end)
        output.append(10)
        hanoi(k - 1, mid, start, end)

    hanoi(n, 1, 2, 3)
    sys.stdout.buffer.write(output)


if __name__ == "__main__":
    main()