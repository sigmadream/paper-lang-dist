import sys

def main():
    s = sys.stdin.readline()
    while s and s[-1] in '\n\r ':
        s = s[:-1]
    if not s:
        return
    print(1 if s == s[::-1] else 0)

main()