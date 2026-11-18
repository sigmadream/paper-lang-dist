import sys

def main():
    data = sys.stdin.read().split()
    if not data:
        return
    t = int(data[0])
    out = []
    for i in range(1, t + 1):
        s = data[i]
        bal = 0
        valid = True
        for c in s:
            if c == '(':
                bal += 1
            else:
                bal -= 1
            if bal < 0:
                valid = False
                break
        if bal != 0:
            valid = False
        out.append("YES" if valid else "NO")
    print("\n".join(out))

main()