import sys

def main():
    data = sys.stdin.read().split()
    if not data:
        return
    t = int(data[0])
    answers = []
    for i in range(1, t + 1):
        s = data[i]
        bal = 0
        valid = True
        for ch in s:
            if ch == '(':
                bal += 1
            else:
                bal -= 1
            if bal < 0:
                valid = False
                break
        if bal != 0:
            valid = False
        answers.append("YES" if valid else "NO")
    sys.stdout.write("\n".join(answers))

if __name__ == "__main__":
    main()