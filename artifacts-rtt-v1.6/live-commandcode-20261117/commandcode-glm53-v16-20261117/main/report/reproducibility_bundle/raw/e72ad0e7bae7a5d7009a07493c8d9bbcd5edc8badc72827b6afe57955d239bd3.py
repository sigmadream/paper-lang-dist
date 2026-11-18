import sys

def main():
    s = sys.stdin.read().split()
    if s:
        print(1 if s[0] == s[0][::-1] else 0)

main()