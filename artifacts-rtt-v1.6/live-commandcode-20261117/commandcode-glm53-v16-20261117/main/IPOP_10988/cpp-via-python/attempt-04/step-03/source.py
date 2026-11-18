import sys

def main():
    s = sys.stdin.readline()
    s = s.rstrip('\n\r ')
    if not s:
        return
    print(1 if s == s[::-1] else 0)

main()