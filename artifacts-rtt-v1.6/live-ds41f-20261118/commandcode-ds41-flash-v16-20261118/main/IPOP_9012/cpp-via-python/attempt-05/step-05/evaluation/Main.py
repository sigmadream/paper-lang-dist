import sys


def main():
    data = sys.stdin.read().split()
    if not data:
        return

    t = int(data[0])
    results = []

    for i in range(1, t + 1):
        s = data[i]
        balance = 0
        valid = True

        for ch in s:
            if ch == '(':
                balance += 1
            else:
                balance -= 1

            if balance < 0:
                valid = False
                break

        if balance != 0:
            valid = False

        results.append("YES" if valid else "NO")

    sys.stdout.write("\n".join(results))


if __name__ == "__main__":
    main()