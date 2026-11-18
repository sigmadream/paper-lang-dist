import sys

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return

    t = int(tokens[0])
    answers = []

    for i in range(1, t + 1):
        s = tokens[i]
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

        answers.append("YES" if valid else "NO")

    sys.stdout.write("\n".join(answers))

if __name__ == "__main__":
    main()