import sys

def main():
    s = sys.stdin.readline().strip()
    print(1 if s == s[::-1] else 0)

if __name__ == "__main__":
    main()