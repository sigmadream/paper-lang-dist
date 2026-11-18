import sys

def main():
    s = sys.stdin.readline()
    if s.endswith('\n'):
        s = s[:-1]
    if s.endswith('\r'):
        s = s[:-1]
    print(1 if s == s[::-1] else 0)

if __name__ == "__main__":
    main()