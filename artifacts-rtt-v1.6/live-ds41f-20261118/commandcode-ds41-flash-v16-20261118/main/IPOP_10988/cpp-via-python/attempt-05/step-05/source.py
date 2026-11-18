import sys

def main():
    data = sys.stdin.read().split()
    if not data:
        return
    s = data[0]
    print(1 if s == s[::-1] else 0)

if __name__ == "__main__":
    main()