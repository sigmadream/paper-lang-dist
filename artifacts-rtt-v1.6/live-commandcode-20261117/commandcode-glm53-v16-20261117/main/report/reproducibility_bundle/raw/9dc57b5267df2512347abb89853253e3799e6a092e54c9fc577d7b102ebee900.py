import sys

def main():
    s = sys.stdin.read().split()
    if s:
        t = s[0]
        print(1 if t == t[::-1] else 0)

main()