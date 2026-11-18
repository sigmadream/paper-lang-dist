import sys


def main():
    data = sys.stdin.read().split()
    if not data:
        return

    t = int(data[0])
    out = []

    for i in range(t):
        s = data[i + 1] if i + 1 < len(data) else ""
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

        out.append("YES" if valid else "NO")

    if out:
        sys.stdout.write("\n".join(out) + "\n")


if __name__ == "__main__":
    main()