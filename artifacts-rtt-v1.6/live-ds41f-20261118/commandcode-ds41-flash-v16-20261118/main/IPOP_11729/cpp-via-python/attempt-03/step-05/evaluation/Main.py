import sys


def main() -> None:
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    n = int(data[0])
    output = []
    output.append(f"{(1 << n) - 1}\n")

    def hanoi(count: int, start: int, mid: int, end: int) -> None:
        if count == 1:
            output.append(f"{start} {end}\n")
            return
        hanoi(count - 1, start, end, mid)
        output.append(f"{start} {end}\n")
        hanoi(count - 1, mid, start, end)

    hanoi(n, 1, 2, 3)
    sys.stdout.write("".join(output))


if __name__ == "__main__":
    main()