import sys

def main():
    s = sys.stdin.read().split()
    if not s:
        return
    s = s[0]
    print(1 if s == s[::-1] else 0)

main()