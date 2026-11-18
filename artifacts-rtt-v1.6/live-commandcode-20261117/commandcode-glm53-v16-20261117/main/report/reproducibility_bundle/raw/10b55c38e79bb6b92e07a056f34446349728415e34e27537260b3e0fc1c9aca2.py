import sys

def main():
    s = sys.stdin.read().split()
    if s:
        s = s[0]
        print(1 if s == s[::-1] else 0)

if __name__ == "__main__":
    main()