import sys

def solve():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    t = int(tokens[0])
    results = []
    for s in tokens[1:t + 1]:
        bal = 0
        valid = True
        for ch in s:
            if ch == '(':
                bal += 1
            elif ch == ')':
                bal -= 1
            if bal < 0:
                valid = False
                break
        if bal != 0:
            valid = False
        results.append("YES" if valid else "NO")
    sys.stdout.write("\n".join(results) + "\n")

if __name__ == '__main__':
    solve()
