import sys

def main():
    data = sys.stdin.read().split()
    s, t = data[0], data[1]
    print(1 if sorted(s) == sorted(t) else 0)

main()