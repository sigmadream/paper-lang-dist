import sys


def main():
    data = sys.stdin.read().split()
    if not data:
        return

    t = int(data[0])
    result = []

    for i in range(1, t + 1):
        s = data[i] if i < len(data) else ""
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

        result.append("YES" if valid else "NO")

    sys.stdout.write("\n".join(result))


if __name__ == "__main__":
    main()