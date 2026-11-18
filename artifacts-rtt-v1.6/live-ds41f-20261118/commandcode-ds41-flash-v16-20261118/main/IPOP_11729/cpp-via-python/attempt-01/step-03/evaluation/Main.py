import sys


def main() -> None:
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    n = int(data[0])

    result = [str((1 << n) - 1) + "\n"]

    def hanoi(k: int, start: int, mid: int, end: int) -> None:
        if k == 1:
            result.append(f"{start} {end}\n")
            return

        hanoi(k - 1, start, end, mid)
        result.append(f"{start} {end}\n")
        hanoi(k - 1, mid, start, end)

    hanoi(n, 1, 2, 3)
    sys.stdout.write("".join(result))


if __name__ == "__main__":
    main()