import sys

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    s = tokens[0]
    print(1 if s == s[::-1] else 0)

if __name__ == "__main__":
    main()