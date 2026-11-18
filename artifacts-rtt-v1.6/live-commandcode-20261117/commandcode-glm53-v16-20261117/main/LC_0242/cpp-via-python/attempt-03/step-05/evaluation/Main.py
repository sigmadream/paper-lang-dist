import sys

def main():
    data = sys.stdin.read().split()
    if len(data) < 2:
        return
    s, t = data[0], data[1]
    print(1 if sorted(s) == sorted(t) else 0)

main()