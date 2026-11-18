import sys


def main() -> None:
    tokens = sys.stdin.read().split()
    if not tokens:
        return

    t = int(tokens[0])
    results = []

    for i in range(t):
        s = tokens[i + 1] if i + 1 < len(tokens) else ""
        balance = 0
        valid = True

        for c in s:
            if c == '(':
                balance += 1
            else:
                balance -= 1

            if balance < 0:
                valid = False
                break

        if balance != 0:
            valid = False

        results.append("YES" if valid else "NO")

    if results:
        sys.stdout.write("\n".join(results) + "\n")


if __name__ == "__main__":
    main()